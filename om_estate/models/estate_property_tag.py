from odoo import fields, models, api
import random

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "estate.property.tag"
    _order = "name desc"

    name = fields.Char(required=True)
    color = fields.Integer(default=lambda self: self._get_next_sequence())

    def _get_next_sequence(self):
        color_number = 1
        if self.search([], limit=1, order='color desc'):
            color_number = self.search([], limit=1, order='color desc').color + 1
        return color_number