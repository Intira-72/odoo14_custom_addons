# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

TODAY_DATE = date.today()
TH_TODAY_DATE = date.today() + relativedelta(years=543)


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'
    _description = 'account.move'


    custom_name = fields.Char("INV Number.")
    inv_to_company = fields.Many2one('res.company', string="INV to Company")


    @api.onchange('invoice_date', 'inv_to_company')
    def _onchange_payment_reference(self):
        
        if self.invoice_date:
            if self.inv_to_company.id == 1:
                inv_date = self.invoice_date + relativedelta(years=543)
            else:
                inv_date = self.invoice_date

            gen_inv_no = self._generate_inv_no(inv_date.strftime('%y%m%d'))
            self.custom_name = f"{inv_date.strftime('%y%m%d')}{gen_inv_no:02}"


    @api.model
    def create(self, vals_list):
        company_id = self.env['sale.order'].search([('name', '=', vals_list['invoice_origin'])]).m_data_file.buyer_id.company_id.id
        
        if self.custom_name == False:
            active_company = self._context.get('allowed_company_ids')[0]

            date_code = TH_TODAY_DATE if (company_id if company_id else active_company) == 1 else TODAY_DATE                  

            vals_list['invoice_date'] = TODAY_DATE
            if company_id:
                vals_list['inv_to_company'] = company_id  
            else:
                vals_list['inv_to_company'] = active_company          

            gen_inv_no = self._generate_inv_no(date_code.strftime('%y%m%d'))
            vals_list['custom_name'] = f"{date_code.strftime('%y%m%d')}{gen_inv_no:02}"

        return super().create(vals_list)


    def _generate_inv_no(self, dt_val):
        last_inv_on_date = self.env['account.move'].search([('custom_name', 'ilike', dt_val)],
                                                            order="invoice_date desc, id desc",
                                                            limit=1)

        if last_inv_on_date:            
            next_inv = int((last_inv_on_date.custom_name.replace(dt_val, ""))) + 1
        else:
            next_inv = 1

        return next_inv

