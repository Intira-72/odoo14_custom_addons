from odoo import models, fields, api, _
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        account_move = self.env['account.move']
        account_move.create(
            {
                'partner_id': self.partner_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    (0, 0, {
                        'name': self.name,
                        'quantity': 1,
                        'price_unit': self.selling_price * 0.06
                    }),
                    (0, 0, {
                        'name': "Administrative Fees",
                        'quantity': 1,
                        'price_unit': 100
                    })
                ]
            }
        )
        
        return super().action_sold()