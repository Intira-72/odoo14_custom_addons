# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


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
    offer_ids = fields.One2many('estate.property.offer', 'property_id')

    total_area = fields.Float(string="Total Area (sqm)", compute='_compute_total_area')
    best_price = fields.Float(string="Best Offer", compute='_compute_best_price')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = self.living_area + self.garden_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for rec in self:
            rec.best_price = max(self.offer_ids.mapped('price'))

    @api.onchange('garden')
    def _onchange_garden(self):
        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = 'north' if self.garden else False


