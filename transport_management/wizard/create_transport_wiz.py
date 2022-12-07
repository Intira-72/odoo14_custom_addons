from odoo import api, fields, models, _
from odoo.exceptions import UserError

class TransportWizard(models.TransientModel):
    _name = "transport.wizard"
    _description = "transport.wizard"

    def get_order_ids(self):
        active_ids = self.env.context.get('active_ids')
        orders = self.env['stock.picking'].browse(active_ids)
        return orders


    def get_operation_type(self):
        try:
            active_ids = self.env.context.get('active_ids')
            o_type = self.env['stock.picking'].browse(active_ids).picking_type_id.id
        except ValueError as err:
            raise UserError(_(err))
        else:
            return o_type


    operation_type = fields.Many2one('stock.picking.type', string="Operation Type", default=get_operation_type, readonly=True)
    vechicle_id = fields.Many2one('transport.vehicles', string="Vechicle", required=True)
    delivery_ids = fields.Many2many('stock.picking', string="Order No.", default=get_order_ids)
    source_id = fields.Many2one('stock.location', string="From", default=8, required=True)
    destination_id = fields.Many2one('stock.location', string="To", default=8, required=True)
    employee_id = fields.Many2one('hr.employee', string="Driver", domain="[('department_id', '=', 'Driver')]", required=True)


    def action_transport_report(self):
        active_ids = self.env.context.get('active_ids')
        rtn = self.env['transport.management']
        
        data = {
            'vechicle_id': self.vechicle_id.id,
            'operation_type': self.operation_type.id,
            'delivery_ids': [(6, 0, active_ids)],
            'source_id': self.source_id.id,
            'destination_id': self.destination_id.id,
            'employee_id': self.employee_id.id
        }

        shipping_id = rtn.create(data) 

        msg = f"Use Delivery No : {' '.join([s.name for s in shipping_id.delivery_ids])}. Created."

        self.env['mail.message'].browse([shipping_id.message_ids.id]).write({'body': msg})

        report_action = self.env['transport.management'].browse(shipping_id.id).action_report_pdf()
        report_action['close_on_report_download'] = True

        return report_action
