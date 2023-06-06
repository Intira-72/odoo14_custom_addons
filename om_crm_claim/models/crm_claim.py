from odoo import fields, models, api, _
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "crm.claim"
    _description = "crm.claim"

    name = fields.Char("Number", readonly=True, required=True, copy=False, default=lambda self: _("New"))
    subject = fields.Char("Subject", required=True)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    claimant = fields.Char("Claimant", required=True)
    phone_num = fields.Char("Phone", required=True)
    claim_date = fields.Datetime(string='Date', required=True, default=fields.Datetime.now)
    order_id = fields.Char(string='Order No.', required=True)
    order_date = fields.Datetime(string='Order Date')
    priority = fields.Selection([('0','Low'), ('1','Normal'), ('2','High')], 'Priority',default='1')
    state = fields.Selection([
        ('new', 'New'),
        ('waiting_back', 'Pending Return'),
        ('in_process', 'In Process'),
        ('in_transit', 'Delivery'),
        ('done', 'Done'),
        ('cancel', 'Canceled')
    ], string='State', default='new')

    @api.model
    def create(self, vals):        
        last_res = self.env['crm.claim'].search([], order="id desc", limit=1)
        if last_res:
            vals['name'] = f"C{last_res.id + 1}" if len(str(last_res)) >= 5 else f'C{"0" * (5 - len(str(last_res)))}{last_res.id}'
        else:
            vals['name'] = "C00001"
        return super().create(vals)