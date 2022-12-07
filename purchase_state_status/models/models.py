# -*- coding: utf-8 -*-

from odoo import models, fields, _, api, registry
from odoo.exceptions import UserError


class purchase_state_status(models.Model):
    _inherit = 'purchase.order'
    _description = 'purchase.order'

    READONLY_STATES = {
        'purchase': [('readonly', True)],
        'received': [('readonly', True)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)],
    }

    state = fields.Selection(selection_add=[('received', 'Received')])
    vendor_ref = fields.Char(related='partner_ref')
    partner_id = fields.Many2one(states=READONLY_STATES)

    def button_confirm(self):
        res = super(purchase_state_status, self).button_confirm()
        if self.vendor_ref:
            return res
        else:
            raise UserError(_(f'"Vendor Reference" is Empty!, Please include the Container No. and the Invoice No.'))
    
    
class StockPicking(models.Model):
    _inherit = 'stock.picking'

    order_id = fields.Char('OP', related='group_id.name')

    def button_validate(self):
        print(self.order_id)
        validation = super(StockPicking, self).button_validate()

        if type(validation) != dict:
            order_obj = self.env['purchase.order'].search([("name", "=", self.order_id)])
            order_obj.write({'state': 'received',
                             'invoice_status': 'to invoice'})

        return validation

