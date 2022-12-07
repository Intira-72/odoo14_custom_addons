# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order'
    #
    # order_l = fields.One2many('purchase.order.line', 'order_id', string='Order Lines')
    # qty_product = fields.Many2one('purchase.order.line', related='order_line.product_qty', string='Product Qty', readonly=True)


class PurchaseOrderLineUnit(models.Model):
    _inherit = 'purchase.order.line'

    @api.onchange('product_qty', 'product_uom')
    def _onchange_quantity(self):
        o_price = self.price_unit
        sup = super(PurchaseOrderLineUnit, self)._onchange_quantity()
        self.price_unit = o_price

        return sup