# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MakroOrders(models.Model):
    _name = 'om_makro_order_import_xml.makro_orders'
    _description = 'om_makro_order_import_xml.makro_orders'

    name = fields.Char("File Name")
    buyer_id = fields.Many2one('om_makro_order_import_xml.makro_buyer')
    order_ids = fields.One2many('sale.order', 'm_data_file', string="Sale Order")


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    m_data_file = fields.Many2one('om_makro_order_import_xml.makro_orders')
