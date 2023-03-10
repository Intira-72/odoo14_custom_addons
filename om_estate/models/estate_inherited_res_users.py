from odoo import fields, models, api, _

class Users(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property', 'user_id', default=None)

    @api.onchange('name')
    def _onchange_(self):
        print(self.property_ids)
        