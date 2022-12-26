from odoo import api, fields, models, _
from odoo.exceptions import UserError

import math

class PurchaseOrderWizard(models.TransientModel):
    _name = "minimum_stock.purchase_order_wiz"
    _description = "minimum_stock.purchase_order_wiz"

    @api.model
    def default_get(self, fields):
        res = super(PurchaseOrderWizard, self).default_get(fields)
        active_id =  self.env.context.get('active_id')

        less_minimum = self.env['below.stock'].browse(active_id)

        res['product_id'] = less_minimum.product_id
        res['required_amount'] = less_minimum.required_amount
        res['order_all_qty'] = less_minimum.required_amount

        return res

    partner_id = fields.Many2one('res.partner', "Customer", required=True)
    product_id = fields.Many2one('product.product', string="Product", readonly=True)
    order_limit = fields.Integer("Qty / Contraner")
    required_amount = fields.Integer("Required Amount", readonly=True)
    count_order = fields.Integer("Order Total", compute="_cal_to_order")
    order_all_qty = fields.Integer("Amount Total", compute="_cal_to_order")
    unit_price = fields.Integer("Unit Price")
    discription = fields.Text("Note")
    

    @api.onchange("order_limit")
    def _cal_to_order(self):        
        if self.order_limit != 0:
            cont_total = math.ceil(round(self.required_amount / self.order_limit))
            if self.required_amount > (self.order_limit * cont_total):
                cont_total += 1

            self.count_order = cont_total
            self.order_all_qty = self.order_limit * cont_total


    def action_create_purchase_order(self):
        purchase_order = self.env['purchase.order']



            # print(math.ceil(round(required_amount / 2000)))
        