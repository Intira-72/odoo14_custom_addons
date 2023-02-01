from odoo import models, fields, api
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
            digit_count = len(str(last_no)) if last_no != 9 else len(str(last_no)) + 1
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
    order_ids = fields.Many2many('sale.order', 'makro_requisition_sale_order_rel', 'order_id', 'requisition_id', string="Order Line")
    active = fields.Boolean(default=True)

    def show_orders(self):
        partner_ids = self.env['om_makro_order_import_xml.makro_store_loc'].search([('zone_id', "=", self.zone_id.id)])
        orders = self.env['sale.order'].search([('commitment_date', "=", self.delivery_date.date()),
                                                ('partner_id', "in", [partner.contact_id.id for partner in partner_ids]),
                                                ('requisition_id', '=', False),
                                                ('state', '=', 'sale')], order='user_id desc')  

        for o in orders:
            self.order_ids = [(4, o.id)]
            o.requisition_id = self.id


    def write(self, vals):      
        try:
            for order in self.order_ids:
                if order.id not in [o for o in vals['order_ids'][0][2]]:
                    order.requisition_id = False

            for order in [o for o in vals['order_ids'][0][2]]:
                if order not in [o.id for o in self.order_ids]:
                    res = self.env['sale.order'].browse(order)
                    res.requisition_id = self.id
        except IndexError:
            pass
        
        return super().write(vals)


    def print_quisition(self):
        file_name = f"MK_{self.zone_id.name}_{self.delivery_date.strftime('%Y%m%d')}"

        report_obj = self.env.ref('om_makro_order_import_xml.report_requisition_xlsx')
        report_obj.report_file = file_name + ".xlsx"
        return report_obj.report_action(self)
     

    class SaleOrder(models.Model):
        _inherit = 'sale.order'

        requisition_id = fields.Many2one('makro.requisition')
