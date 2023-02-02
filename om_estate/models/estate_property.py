# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate.property"

    name = fields.Char(string="Name", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date(string="Available From", copy=False, default=fields.Date.today().replace(month=+3))
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
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
    active = fields.Boolean(default=True)
    state = fields.Selection(selection=[('new', 'New'),
                                        ('received', 'Offer Received'),
                                        ('accepted', 'Offer Accepted'),
                                        ('sold', 'Sold'),
                                        ('canceled', 'Canceled')], default='new', copy=False)

    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    user_id = fields.Many2one('res.users', string="Salesman",default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string="Buyer")

    tag_ids = fields.Many2many('estate.property.tag')
