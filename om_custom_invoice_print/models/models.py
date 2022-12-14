# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

TODAY_DATE = date.today()
TH_TODAY_DATE = date.today() + relativedelta(years=543)

class AccountMoveInherit(models.Model):
    _inherit = 'account.move'
    _description = 'account.move'

    def _get_company(self):
        return self.env.company

    custom_name = fields.Char("INV Number.", readonly=True)
    inv_to_company = fields.Many2one('res.company', string="INV to Company", default=_get_company)

    @api.onchange('invoice_date')
    def _onchange_payment_reference(self):
        if self.invoice_date:
            if self.inv_to_company.id == 1:
                inv_date = self.invoice_date + relativedelta(years=543)
            else:
                inv_date = self.invoice_date

            count_inv = self.env['account.move'].search([('invoice_date', '=', self.invoice_date)])
            self.custom_name = f"{inv_date.strftime('%y%m%d')}{len(count_inv):02}"

    @api.model
    def create(self, vals_list):
        if self.custom_name == False:
            count_inv = self.env['account.move'].search([('invoice_date', '=', TODAY_DATE)])
            vals_list['invoice_date'] = TODAY_DATE

            if self.inv_to_company.id == 2:                
                vals_list['custom_name'] = f"{TH_TODAY_DATE.strftime('%y%m%d')}{len(count_inv):02}"
            else:
                vals_list['custom_name'] = f"{TODAY_DATE.strftime('%y%m%d')}{len(count_inv):02}"

        return super().create(vals_list)

    def custom_inv_print(self):
        return self.env.ref('om_custom_invoice_print.action_custom_inv_print').report_action()

