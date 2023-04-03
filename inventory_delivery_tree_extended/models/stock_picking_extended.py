# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    _order = 'name desc'

    customer_ref = fields.Char("PO No.", compute="_compute_vendor_ref", search="_search_ref")


    @api.depends('store')
    def _compute_vendor_ref(self):
        for ori in self:
            if ori.picking_type_id.name == "Receipts":
                v_ref = self.env['purchase.order'].search([('name', '=', ori.group_id.name)])
                ori.customer_ref = v_ref.partner_ref
            elif ori.picking_type_id.name == "Delivery Orders":
                cus_ref = self.env['sale.order'].search([('name', '=', ori.group_id.name)])
                ori.customer_ref = cus_ref.client_order_ref
                ori.store = cus_ref.store_id.id
            else:
                ori.customer_ref = False

    
    def _search_ref(self, operator, value):   
        picking_type = self.env.context.get('active_id', False)

        ids = []
        
        if picking_type == 1:
            rtn = self.env['purchase.order'].search([('partner_ref', 'ilike', value)])
        elif picking_type == 2:
            rtn = self.env['sale.order'].search([('client_order_ref', 'ilike', value)])

        for r in rtn:
                for i in r:
                    [ids.append(o.id) for o in self.search([('origin', '=', i.name)])]
        
        return [('id', 'in', ids)]
