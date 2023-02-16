from odoo import fields, models, api, _
from odoo.exceptions import UserError

class Partner(models.Model):
    _inherit = 'res.partner'

    reservation_stock_partner = fields.Many2one('stock.location', string="Reservation Location")