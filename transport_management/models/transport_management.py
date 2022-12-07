# -*- coding: utf-8 -*-


from email.policy import default
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class TransportManagement(models.Model):
    _name = 'transport.management'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Delivery Note'
    _order = 'id desc'

    name = fields.Char("Transport No.", compute="_compute_get_name")
    operation_type = fields.Many2one('stock.picking.type', string="Operation Type", readonly=True)
    vechicle_id = fields.Many2one('transport.vehicles', string="Vechicle", required=True, readonly=False, states={'cancel': [('readonly', True)]})
    delivery_ids = fields.Many2many('stock.picking', string="Order No.", readonly=False, states={'cancel': [('readonly', True)]})
    source_id = fields.Many2one('stock.location', string="From", required=True, readonly=False, states={'cancel': [('readonly', True)]})
    destination_id = fields.Many2one('stock.location', string="To", required=True, readonly=False, states={'cancel': [('readonly', True)]})
    employee_id = fields.Many2one('hr.employee', string="Driver", readonly=False, states={'cancel': [('readonly', True)]})
    state = fields.Selection([
        ('done', 'Done'),
        ('cancel', 'Cancelled')], default='done')


    def _compute_get_name(self):
            for rec in self:
                id_to_char = str(rec.id)
                rec.name = "DN" + id_to_char if len(id_to_char) == 5 else "DN" + ("0" * (5 - len(id_to_char))) + id_to_char


    def action_report_pdf(self):
        order_lists = []
        
        for order in self.delivery_ids:
            try:
                if order.is_shipping == 0:
                    order_lists.append({'reference': f"{order.name}",
                                        'create_date': f"{order.create_date.strftime('%Y-%m-%d')}",
                                        "origin": order.origin})

                    order.write({'is_shipping': 1})
                else:
                    raise ValueError(_(f"The delivery no: {order.name} has been used, please check the information."))
            except ValueError as err:
                raise UserError(_(err))            

        data = {'name': self.name,
                'vechicle_id': f"{self.vechicle_id.vehicle_reg}",
                'from_loc': f"{self.source_id.name}",
                'to_loc': f"{self.destination_id.name}",
                'operation_type': f"{self.operation_type.name}",
                'order_lists': order_lists,
                'employee_id': f"{self.employee_id.name}",
                'u_id': self.create_uid.name}

        
        report_action = self.env.ref('transport_management.transport_report_action').report_action(self, data=data) 
        report_action['print_report_name'] = self.name
        
        return report_action

    def write(self, val_list):
        o_data = {'vechicle_id': self.vechicle_id,
                'employee_id': self.employee_id,
                'source_id': self.source_id,
                'destination_id': self.destination_id,
                'delivery_ids': self.delivery_ids}
        
    
        rtn = super(TransportManagement, self).write(val_list)
        n_data = self.env['transport.management'].browse(self.id)

        msg = []        

        if o_data['vechicle_id'] != n_data.vechicle_id:
            msg.append(self._get_msg('Car', o_data['vechicle_id'].vehicle_reg, n_data.vechicle_id.vehicle_reg))

        if o_data['employee_id'] != n_data.employee_id:
            msg.append(self._get_msg('Driver', o_data["employee_id"].name, n_data.employee_id.name))

        if o_data['source_id'] != n_data.source_id:
            msg.append(self._get_msg('Source Location', o_data["source_id"].name, n_data.source_id.name))

        if o_data['destination_id'] != n_data.destination_id:
            msg.append(self._get_msg('Desination Location', o_data["destination_id"].name, n_data.destination_id.name))

        if o_data['delivery_ids'] != self.delivery_ids:
            val_dif = set(o_data['delivery_ids']) ^ set(self.delivery_ids)
            msg_del = []
            msg_add = []
            for v in val_dif:
                if v in o_data['delivery_ids']:
                    msg_del.append(v.name)
                    v.is_shipping = 0
                else:
                    print(f"Add {v.name}")
                    msg_add.append(v.name)
                    v.is_shipping = 1

            if msg_del != []:
                msg.append(self._get_msg('Remove', ' '.join(msg_del), ''))

            if msg_add != []:
                msg.append(self._get_msg('Add', ' '.join(msg_add), ''))
        
        if self.state == 'done':
            self.message_post(body=f"<div><ul>{''.join(msg)}</ul></div>")
        
        return rtn

    def button_cancel(self):
        self.state = 'cancel'

        for line in self.delivery_ids:
            line.write({'is_shipping': 0})

        self.message_post(body=f"<div><ul><li>Canceled</il></ul></div>")
        
        return True

    def unlink(self):
        for order in self.delivery_ids:
            order.is_shipping = 0

        return super(TransportManagement, self).unlink()

    def _get_msg(self, topic, o_data, n_data):
        if n_data == '':
            msg = _("<li><strong>%s : </strong> %s.</li>") % (topic, o_data)
        else:
            msg = _("<li><strong>%s : </strong> %s <strong>&rarr;</strong> %s.</li>") % (topic, o_data, n_data)

        return msg


class StockPicking(models.Model):
    _inherit = "stock.picking"

    is_shipping = fields.Boolean("Shipping Status", default=0, store=True)

    def action_open_transport_wiz(self):
        return {
            'name': "PDF Shipping",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'transport.wizard',
            'view_id': self.env.ref('transport_management.create_transport_wiz_form').id,
            'target': 'new'
        }

