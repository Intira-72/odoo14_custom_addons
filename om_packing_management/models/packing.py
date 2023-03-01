from odoo import fields, models, api, _
from odoo.exceptions import UserError


class Packing(models.Model):
    _name = 'stock.packing'
    _description = 'stock.packing'

    name = fields.Char()

    

