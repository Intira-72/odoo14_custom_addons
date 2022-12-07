# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.osv import expression


class TransportVehicles(models.Model):
    _name = 'transport.vehicles'
    _description = 'transport.vehicles'

    def _get_default_type(self):
        try:
            rtn = self.env['transport.vehicle.types'].search([])
            return rtn[0].id
        except IndexError:
            raise UserError(_("The transport type was not found."))

    name = fields.Char("Vehicle No.", compute='_compute_vehicle_no', readonly=True)
    vehicle_reg = fields.Char("Vehicles Code", required=True, unique=True)
    vehicle_type = fields.Many2one('transport.vehicle.types', string="Category", default=_get_default_type, required=True)
    is_active = fields.Boolean(default=True)

    def _compute_vehicle_no(self):
        vehicle_code = "VE"
        if self:
            for line in self:
                line.name = vehicle_code + str(line.id) if len(str(line.id)) == 3 else f"{vehicle_code}{'0' * (3 - len(str(line.id)))}{str(line.id)}"
            return True 


    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, f"[{record.vehicle_reg}] {record.vehicle_type.name}"))

        return result

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        """ search Registoration and Category name """
        args = args or []
        domain = []
        if name:
            domain = ['|', ('vehicle_reg', operator, name), ('vehicle_type.name', operator, name)]
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)   
    
    
class TransportVehicleTypes(models.Model):
    _name = 'transport.vehicle.types'
    _description = 'transport.vehicle.types'

    name = fields.Char("Name", required=True)
    container_width = fields.Float("Width (M)")
    container_length = fields.Float("Lenght (M)")
    container_height = fields.Float("Height (M)")
    container_size = fields.Float("Container Size (CBM)", compute='_compute_picking_size_cal', readonly=True)
    weight_limit = fields.Float("Weight Limit (T)")
    is_active = fields.Boolean(default=True)


    @api.onchange('container_width', 'container_length', 'container_height')
    def _compute_picking_size_cal(self):
        for line in self:
            line.container_size = line.container_width * line.container_length * line.container_height
        