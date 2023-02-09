from odoo import fields, models, api


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "estate.property.tag"
    _order = "name desc"

    name = fields.Char(required=True)
    color = fields.Integer(default=lambda self: self.env.id + 1)

    