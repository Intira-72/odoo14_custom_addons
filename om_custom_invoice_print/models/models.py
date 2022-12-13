# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date, timedelta


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'
    _description = 'account.move'

    @api.model
    def _default_custom_num(self):
        dt = date.today()
        count_inv = self.env['account.move'].search([('invoice_date', '=', dt)])
        inv_no = dt.strftime('%y%m%d')
        return f'{inv_no}{len(count_inv):02}'

    custom_name = fields.Char("INV Number.")

    def custom_inv_print(self):
        return self.env.ref('om_custom_invoice_print.action_custom_inv_print').report_action(None)

    @api.onchange('invoice_date')
    def _onchange_payment_reference(self):
        if self.invoice_date:
            count_inv = self.env['account.move'].search([('invoice_date', '=', self.invoice_date)])
            self.custom_name = f"{self.invoice_date.strftime('%y%m%d')}{len(count_inv):02}"

    @api.model
    def create(self, vals_list):
        if self.custom_name == '':
            count_inv = self.env['account.move'].search([('invoice_date', '=', self.invoice_date)])
            self.custom_name = f"{self.invoice_date.strftime('%y%m%d')}{len(count_inv):02}"
        return super().create(vals_list)

