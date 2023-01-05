from odoo import api, fields, models, _
from odoo.exceptions import UserError
from io import BytesIO

import xml.etree.ElementTree as et
import base64


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
                if not rtn.search([('client_order_ref', '=', data['po_number'])]):
                    order_id = rtn.create(sale_order)  
            else:
                raise ValueError(_(f"PO No.{data['po_number']}:\n - Delivery address not found."))
        except ValueError as err:
            raise UserError(_(err))
        else:
            return order_id


    def _check_m_code(self, xroot):
        err_lists = []
        for node in xroot:             
            for po in node.findall('POHEADER'):
                for line in po.findall('POLINE'):
                    pro_ids = self.env['om_makro_order_import_xml.makro_products'].search([('makro_code', '=', line.find('BUYERARTNO').text)]).product_ids
                    if not pro_ids:
                        rtn = self.env['om_makro_order_import_xml.makro_products']

                        if not rtn.search([('makro_code', '=', line.find('BUYERARTNO').text)]):
                            rtn.create({'makro_code': line.find('BUYERARTNO').text,
                                        'name': line.find('PRODUCTDESCRIPTION').text})
                            self.env.cr.commit()

                        msg = f"Code: {line.find('BUYERARTNO').text} Name: {line.find('PRODUCTDESCRIPTION').text}"
                        if msg not in err_lists:
                            err_lists.append(msg)        
        if err_lists:
            return "\n".join(err_lists)
        else:
            return True        


    def _oder_line(self, order_line):                     
        order_line_id = self.env['sale.order.line'].create(order_line)
        return order_line_id


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
            else:
                if product_ids:
                    se_product_id = {'pid': product_ids[0].id, 'sum_s': 0}

        return se_product_id['pid']


    def _upload_list(self, order_ids, buyer_id):
        rtn = self.env['om_makro_order_import_xml.makro_orders']
        return rtn.create({'name': self.file_name,
                            'order_ids': [(4, i) for i in order_ids],
                            'buyer_id': buyer_id})


    def action_import_orders(self):
        file = self._call_file_xml()  
        
        if file:
            xroot = et.parse(BytesIO(base64.b64decode(file.datas))).getroot()
            order_ids = []

            err_msg = self._check_m_code(xroot)                    
                      
            if type(err_msg) is not str:
                for node in xroot:
                    for po in node.findall('POHEADER'):
                        data = {'store_no': po.find('STORENO').text,
                                'po_number': po.find('PONO').text,
                                'po_date': po.find('PODATE').text,
                                'ship_to_date': po.find('SHIPTODATE').text,
                                'buyer_code': po.find('BUYERINTERNALCODE').text,
                                'paymentterm': po.find('PAYMENTTERMS').text,
                                }

                        order_id = self._create_order(data)
                        for line in po.findall('POLINE'):
                            pro_ids = self.env['om_makro_order_import_xml.makro_products'].search([('makro_code', '=', line.find('BUYERARTNO').text)]).product_ids
                            max_stock = self._auto_select_product_the_mose(pro_ids)

                            order_line = {
                                'order_id': order_id.id,
                                'product_id': max_stock,
                                'product_uom_qty': line.find('ORDERQUANTITY').text
                            }
                            self._oder_line(order_line)

                self._upload_list(order_ids, self.env['om_makro_order_import_xml.makro_buyer'].search([('name', '=', po.find('BUYERINTERNALCODE').text,)]).id)
            else:
               raise UserError(err_msg)        

            file.unlink()
            return {
                    'type': 'ir.actions.client',
                    'tag': 'reload',
                    }                 
                
        else:
           raise UserError('An uploaded file with the same name was found.')


