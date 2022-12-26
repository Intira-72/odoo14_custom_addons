from odoo import api, fields, models, _
from odoo.exceptions import UserError
import xml.etree.ElementTree as et 

import pandas as pd
import base64
from io import BytesIO

class MakroImportOrdersWizard(models.TransientModel):
    _name = "makro_orders.wizard"
    _description = "makro_orders.wizard"

    file_data = fields.Binary(string="Upload File")
    file_name = fields.Char('File Name')

    def _create_file_binary(self):
        if self.env['om_makro_order_import_xml.makro_orders'].search([('name', '=', self.file_name)]):
            return False
        else:
            save_file = self.env['ir.attachment'].create({
                        'name': self.file_name,
                        'type': 'binary',
                        'datas': self.file_data,
                    })    
            return save_file.id


    def _call_file_xml(self):
        xml_file = self.env['ir.attachment'].sudo().search([('id', '=', self._create_file_binary())])
        return xml_file

    def _create_order(self, data):
        # rtn = self.env['om_makro_order_import_xml.makro_orders']
        rtn = self.env['sale.order']
        buyer_id = self.env['om_makro_order_import_xml.makro_buyer'].search([('name', '=', data['buyer_code'])])
        location_id = self.env['om_makro_order_import_xml.makro_store_loc'].search([('name', '=', data['store_no'])])
        payment_term_id = self.env['account.payment.term'].search([('name', '=', data['paymentterm'])])
        
        try:
            if location_id:
                sale_order = {'client_order_ref': data['po_number'],
                                'date_order': data['po_date'],
                                'commitment_date': data['ship_to_date'],
                                'partner_id': location_id.contact_id.id,
                                'payment_term_id': payment_term_id.id}

                order_id = rtn.create(sale_order)  
            else:
                raise ValueError(_(f"PO No.{data['po_number']}:\n - Delivery address not found."))
        except ValueError as err:
            raise UserError(_(err))
        else:
            return order_id


    def _oder_line(self, file, order_no):
        order_lines = pd.read_xml(BytesIO(base64.b64decode(file.datas)), xpath=".//POLINE")
        line_by_order = order_lines.loc[order_lines['PONO'] == float(order_no.client_order_ref)]

        order_line = []
        for line in line_by_order.values:
            try:
                pro_ids = self.env['om_makro_order_import_xml.makro_products'].search([('makro_code', '=', line[5])]).product_ids
                product_id_list = [i.product_id for i in pro_ids]

                if pro_ids:
                    order_line = {'order_id': order_no.id,
                                    'product_id': self._auto_select_product_the_mose(product_id_list),
                                    'product_uom_qty': line[10]}
                else:
                    raise ValueError(_(f"PO No. {order_no.name}:\n - [{line[5]}] {line[7]}\nProduct not found."))
            except ValueError as err:
               raise UserError(err)
            else:        
                self.env['sale.order.line'].create(order_line)
                return True


    def _auto_select_product_the_mose(self, product_ids):
        se_product_id = {}

        for product_id in product_ids:
            quants = self.env['stock.quant'].search([('product_id', '=', product_id.id), ('quantity', '>', 0), ('on_hand', '=', True)])           

            if quants:
                pid = 0
                sum_s = 0
                for quant in quants:
                    pid = quant.product_id.id
                    sum_s += quant.quantity
        
                if se_product_id == {}:
                    se_product_id = {'pid': pid, 'sum_s': sum_s}
                else:
                    if se_product_id['sum_s'] < sum_s:
                        se_product_id = {'pid': pid, 'sum_s': sum_s}

        return se_product_id['pid']


    def _upload_list(self, order_ids, buyer_id):
        print(buyer_id)
        rtn = self.env['om_makro_order_import_xml.makro_orders']
        return rtn.create({'name': self.file_name,
                            'order_ids': [(4, i) for i in order_ids],
                            'buyer_id': buyer_id})


    def action_import_orders(self):
        file = self._call_file_xml()        

        if file:
            order_datas = pd.read_xml(BytesIO(base64.b64decode(file.datas)), xpath=".//POHEADER")
            order_ids = []
            buyer_id = ''
            for order in order_datas.values:
                data = {'store_no': order[1],
                        'po_number': str(order[2]),
                        'po_date': order[3],
                        'ship_to_date': order[4],
                        'buyer_code': str(order[7]),
                        'paymentterm': f'{order[9]} Days',
                        }
                order_id = self._create_order(data)
                self._oder_line(file, order_id)         
                order_ids.append(order_id.id)

                if buyer_id == '':
                    buyer_id = str(order[7])

            self._upload_list(order_ids, self.env['om_makro_order_import_xml.makro_buyer'].search([('name', '=', buyer_id)]).id)
            file.unlink()

            return {
                    'type': 'ir.actions.client',
                    'tag': 'reload',
                    }
        else:
           raise UserError('An uploaded file with the same name was found.')
