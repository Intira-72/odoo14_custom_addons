from odoo import fields, models, api, _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "estate.property.offer"
    _sql_constraints = [('check_price', 'CHECK(price > 0)', 'A property Price must be strictly positive')]

    price = fields.Float()
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=True)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends('validity')
    def _compute_date_deadline(self):
        for rec in self:
            try:
                rec.date_deadline = rec.create_date.date() + timedelta(days=rec.validity)
            except AttributeError:
                rec.date_deadline = datetime.today() + timedelta(days=rec.validity)

    def _inverse_date_deadline(self):
        for rec in self:
            rec.date_deadline = rec.date_deadline


    def action_accepted(self):
        for rec in self:
            rec.status = 'accepted'
            rec.property_id.selling_price = rec.price
            rec.property_id.partner_id = rec.partner_id

            for offer in rec.property_id.offer_ids:
                if offer.id != rec.id:
                    offer.status = 'refused'

        return True
    
    def action_refused(self):
        for rec in self:
            rec.status = 'refused'
            rec.property_id.selling_price = 0
            rec.property_id.partner_id = False

        return True
    

    @api.constrains('status')
    def _check_selling_price(self):
        for rec in self:
            selling = (rec.property_id.expected_price * 90) / 100

            if rec.price < selling and rec.status == 'accepted':
                raise ValidationError(f"The selling price must be greater than 90% of the expected price.")
            
        return True