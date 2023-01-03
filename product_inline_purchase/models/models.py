# -*- coding: utf-8 -*-

from odoo import models, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.onchange('product_qty', 'product_uom')
    def _onchange_quantity(self):
        o_price = self.price_unit
        res = super(PurchaseOrderLine, self)._onchange_quantity()      

        if self.create_uid.id != False:
            self.price_unit = o_price

        return res
