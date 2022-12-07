# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api, _


class SaleOrderLine(models.Model):   
    _inherit = "sale.order.line"
    
    order_ids = fields.Char('Order Reference', related='order_id.name', store=True)
    customer_ref = fields.Char('Customer Reference', related='order_id.client_order_ref', store=True)
    customer_id = fields.Many2one('res.partner', related='order_id.partner_id')
    order_state = fields.Selection('Status', related='order_id.state')
    on_hand_today = fields.Float('On Hand', related='qty_available_today')


    def confirm_orders(self):
        active_ids = self.env.context.get('active_ids')
        order_id = list(dict.fromkeys([o.id for o in self.env['sale.order.line'].browse(active_ids).order_id]))

        rtn = self.env['sale.order'].browse(order_id)

        for order in rtn:
            order.action_confirm()

            picking = self.env['stock.picking'].search([('sale_id.id', '=', order.id)])
            picking.action_assign()


            
