from odoo import fields, models, api, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    reservation_state = fields.Boolean(default=False)    

    def action_selected_location(self):
        for rec in self:
            rec.reservation_state = False if rec.reservation_state else True