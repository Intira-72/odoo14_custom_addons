from odoo import fields, models, api, _
from odoo.exceptions import UserError

class Picking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def create(self, vals):
        print(vals)
        return super().create(vals)