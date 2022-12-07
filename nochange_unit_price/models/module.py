# -*- coding: utf-8 -*-

from odoo import models, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.onchange('product_qty', 'product_uom')
    def _onchange_quantity(self):
        o_unit_price = self.price_unit
        sup = super(PurchaseOrderLine, self)._onchange_quantity()
        self.price_unit = o_unit_price

        return sup
