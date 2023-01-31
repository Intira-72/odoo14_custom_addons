from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools import date_utils

from datetime import datetime, timedelta

DATETIME_NOW = datetime.now()

class MakroRequisition(models.Model):
    _name = 'makro.requisition'
    _description = 'makro.requisition'
    _order = 'id desc'


    def get_name_default(self):
        first_day = DATETIME_NOW.replace(day=1)
        last_day = DATETIME_NOW.replace(month=DATETIME_NOW.month+1, day=1) - timedelta(days=1)

        try:
            get_last = self.env['makro.requisition'].search([('create_date', '>=', first_day.date()), ('create_date', '<=', last_day.date())], order='create_date desc', limit=1)
            
            last_no = int(get_last.name[4:])
            digit_count = len(str(last_no))
            new_no = str(last_no + 1) if digit_count == 3 else "0"*(3 - digit_count) + str(last_no + 1)
        except TypeError:
            return DATETIME_NOW.strftime("%y%m") + "001"
        except IndexError:
            return DATETIME_NOW.strftime("%y%m") + "001"
        else:            
            return DATETIME_NOW.strftime("%y%m") + new_no


    name = fields.Char("No.", default=get_name_default, readonly=True)
    delivery_date = fields.Datetime("Scheduled Date", required=True, default=fields.Datetime.now)
    zone_id = fields.Many2one('makro.location_zone', string="Zone", default=1, required=True)
    order_ids = fields.One2many('sale.order', 'requisition_id', compute="_onchange_scheduled_date", string="Order Line")


    @api.onchange('delivery_date', 'zone_id')
    def _onchange_scheduled_date(self):
        partner_ids = self.env['om_makro_order_import_xml.makro_store_loc'].search([('zone_id', "=", self.zone_id.id)])
        orders = self.env['sale.order'].search([('commitment_date', "=", self.delivery_date.date()),
                                                ('partner_id', "in", [partner.contact_id.id for partner in partner_ids]),
                                                ('state', '=', 'sale')], order='user_id desc')        
        self.order_ids = orders
   

    def print_quisition(self):
        file_name = f"MK_{self.zone_id.name}_{self.delivery_date.strftime('%Y%m%d')}"

        report_obj = self.env.ref('om_makro_order_import_xml.report_requisition_xlsx')
        report_obj.report_file = file_name + ".xlsx"
        return report_obj.report_action(self)
     

    class SaleOrder(models.Model):
        _inherit = 'sale.order'

        requisition_id = fields.Many2one('makro.requisition')
