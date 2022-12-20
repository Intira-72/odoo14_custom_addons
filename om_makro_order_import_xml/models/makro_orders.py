# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MakroOrders(models.Model):
    _name = 'om_makro_order_import_xml.makro_orders'
    _description = 'om_makro_order_import_xml.makro_orders'

    name = fields.Char("Makro PO.")
    po_date = fields.Date("PO Date")
    contact_id = fields.Many2one('om_makro_order_import_xml.makro_store_loc', string="Location")
    schedule_date = fields.Date("Schedule Date")
    buyer_id = fields.Many2one('om_makro_order_import_xml.makro_buyer', string="Buyer Code")   
    order_line_ids = fields.One2many('om_makro_order_import_xml.makro_order_line', 'm_order_id')
    # payment_term = fields.Integer("Payment Term")

    def name_get(self):
        result = []            
            
        for rec in self:
            result.append((rec.id, 'PO%s' % (rec.name)))
        return result
    

class MakroOrderLine(models.Model):
    _name = 'om_makro_order_import_xml.makro_order_line'
    _description = 'om_makro_order_import_xml.makro_order_line'

    
    m_order_id = fields.Many2one('om_makro_order_import_xml.makro_orders', string="Order")
    product_id = fields.Many2one('om_makro_order_import_xml.makro_products', string="Product")
    order_qty = fields.Integer("Total")