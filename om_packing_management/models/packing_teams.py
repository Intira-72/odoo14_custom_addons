from odoo import fields, models, api, _
from odoo.exceptions import UserError


class PackingTeam(models.Model):
    _name = 'stock.packing.teams'
    _description = 'stock.packing.teams'

    name = fields.Char('Team', required=True)
    employee_ids = fields.One2many('stock.packing.employee', 'packing_team_id')


class Employee(models.Model):
    _name = 'stock.packing.employee'
    _description = 'stock.packing.employee'

    packing_team_id = fields.Many2one('stock.packing.teams')
    employee_id = fields.Many2one('hr.employee', required=True)