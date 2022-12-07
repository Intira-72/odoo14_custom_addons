# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'


    def open_wiz_merge(self):

        return self.env['ir.actions.act_window']._for_xml_id('merge_delivery_order.stock_merge_delivery_action')
