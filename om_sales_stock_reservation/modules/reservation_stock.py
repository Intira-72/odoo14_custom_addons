from odoo import fields, models, api, _
from odoo.exceptions import UserError


class SaleStockReservations(models.Model):
    _name = "sale.stock.reservations"
    _description = "sale.stock.reservations"

    name = fields.Char()