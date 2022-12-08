import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class TransportReportWizard(models.TransientModel):
    _name = "transport.report.wizard"
    _description = "transport.report.wizard"

    employee_id = fields.Many2one('hr.employee', string="Driver")
    operation_type = fields.Many2one('stock.picking.type', string="Operation Type")
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)


    def _filter_data_for_report(self):
        search_data = [i for i in [('employee_id', '=', self.employee_id.id),
                        ('operation_type', '=', self.operation_type.id),
                        ('create_date', '>=', self.start_date),
                        ('create_date', '<=', self.end_date),
                        ('state', '=', 'done')] if False not in i]

        rtn = self.env['transport.management'].search(search_data)

        return rtn


    def _report_lists(self):        
        data = self._filter_data_for_report()
        partner_list = list(dict.fromkeys([partner.employee_id.id for partner in data]))

        report_all_list = []

        for by_partner in partner_list:
            ls = []
            for data_line in data:
                if data_line.employee_id.id == by_partner:
                    ls.append(data_line)

            report_all_list.append({'partner': self.env['hr.employee'].browse(by_partner).name,
                                    'delivery_round': len([l for l in ls if l[0].operation_type.id == 2]),
                                    'internal_round': len([l for l in ls if l[0].operation_type.id == 5])})

        return report_all_list


    def _report_by_partner(self):
        data = self._filter_data_for_report()
        report_list = []

        for i in data:
            report_list.append({'date_create': i.create_date.strftime("%d/%m/%Y"),
                                'doc_name': i.name,
                                'vechicle_id': i.vechicle_id.vehicle_reg,
                                'operation_type': i.operation_type.name})

        return report_list

    def report(self):
        if self.employee_id.name == False:
            report_list = self._report_lists()
        else:
            report_list = self._report_by_partner()


        dt_start = self.start_date.strftime("%d %B %Y")
        dt_end = self.end_date.strftime("%d %B %Y")

        data = {'report_date': self.create_date.strftime("%A %d %B %Y"),
                'cycle_of_month': f"{dt_start} - {dt_end}",
                'driver': 'ALL' if self.employee_id.name == False else self.employee_id.name,
                'operation_type': 'ALL' if self.operation_type.name == False else self.operation_type.name,
                'report_list': report_list,
                'report_by': self.env.user.name,
                'count_r': len(report_list)}
        
        report_action = self.env.ref('transport_management.action_report_of_month').report_action(self, data=data) 
        report_action['close_on_report_download'] = True
        
        return report_action
