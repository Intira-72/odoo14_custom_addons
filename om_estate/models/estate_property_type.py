from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property.type"
    _description = "estate.property.type"

    name = fields.Char("Property Type", required=True)