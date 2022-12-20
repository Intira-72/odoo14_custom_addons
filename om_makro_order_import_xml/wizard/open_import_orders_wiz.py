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
        rtn = self.env['om_makro_order_import_xml.makro_orders']
        buyer_id = self.env['om_makro_order_import_xml.makro_buyer'].search([('name', '=', data['buyer_code'])])
        location_id = self.env['om_makro_order_import_xml.makro_store_loc'].search([('name', '=', data['store_no'])])

        order_id = rtn.create({'name': data['po_number'],
                    'po_date': data['po_date'],
                    'schedule_date': data['ship_to_date'],
                    'buyer_id': buyer_id.id,
                    'contact_id': location_id.id})  

        return order_id


    def _oder_line(self, file, order_no):
        order_lines = pd.read_xml(BytesIO(base64.b64decode(file.datas)), xpath=".//POLINE")
        line_by_order = order_lines.loc[order_lines['PONO'] == float(order_no.name)]

        order_line = []
        for line in line_by_order.values:
            product_id = self.env['om_makro_order_import_xml.makro_products'].search([('makro_code', '=', line[5])])
            order_line.append((0, 0, {'product_id': product_id.id,
                                'order_qty': line[10]}))
        
        order_no.write({'order_line_ids': order_line})

        return True


    def action_import_orders(self):
        file = self._call_file_xml()
        order_datas = pd.read_xml(BytesIO(base64.b64decode(file.datas)), xpath=".//POHEADER")

        for order in order_datas.values:
            data = {'store_no': order[1],
                    'po_number': str(order[2]),
                    'po_date': order[3],
                    'ship_to_date': order[4],
                    'buyer_code': str(order[7]),
                    'paymentterm': order[9]}

            self._oder_line(file, self._create_order(data))         
        
        file.unlink()

        return {
                'type': 'ir.actions.client',
                'tag': 'reload',
                }
