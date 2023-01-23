from odoo import api, fields, models, _


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    source_doc = fields.Char(related='picking_id.origin', related_sudo=False, readonly=False)