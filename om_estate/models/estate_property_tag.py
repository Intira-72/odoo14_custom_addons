from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "estate.property.tag"
    _order = "name desc"

    name = fields.Char(required=True)