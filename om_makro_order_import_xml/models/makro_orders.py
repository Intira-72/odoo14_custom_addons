# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class MakroOrders(models.Model):
    _name = 'om_makro_order_import_xml.makro_orders'
    _description = 'om_makro_order_import_xml.makro_orders'
    _order = 'id desc'

    name = fields.Char("File Name")
    buyer_id = fields.Many2one('om_makro_order_import_xml.makro_buyer')
    order_ids = fields.One2many('sale.order', 'm_data_file', string="Sale Order", readonly=True)

    
    def _check_confirm_in_order_lists(self, order_lists):
        order_state = list(dict.fromkeys(order_lists))

        if not 'draft' in order_state:
            return False
        elif len(order_state) > 1:
            return False
        else:
            return True


    def unlink(self):
        if self._check_confirm_in_order_lists([o.state for o in self.order_ids]):
            for order in self.order_ids:
                order.unlink()
        
            result = super(MakroOrders, self).unlink()    
            return result    
        else:
           raise UserError('All State Is Not "Draft"')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    m_data_file = fields.Many2one('om_makro_order_import_xml.makro_orders')
