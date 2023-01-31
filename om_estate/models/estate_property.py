# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate.property"

    name = fields.Char(string="Name", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Post Code")
    date_availability = fields.Date(copy=False, default=fields.Date.today().replace(month=+3))
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(string='Type',
                                            selection=[('north', 'North'),
                                                        ('south', 'South'),
                                                        ('east', 'East'),
                                                        ('west', 'West')],
                                            help="")
        