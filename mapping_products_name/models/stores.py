# -*- coding: utf-8 -*-
from odoo import models, fields, api


class store_list(models.Model):
    _name = 'store.list'
    _description = 'mapping_product_name.store_list'

    name = fields.Char('Store Name', required=True)
    store_group_id = fields.Many2one('res.partner', string='Group')
    

class Partner(models.Model):
    _inherit = 'res.partner'

    store_ids = fields.One2many('store.list', 'store_group_id', string='SHOP')


class ImportFileData(models.Model):
    _name = 'import.file.data'
    _description = 'mapping_product_name.import_file_data'

    name = fields.Char("File", unique=True)

    
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _order = 'id desc'

    store_id = fields.Many2one('store.list', string='By SHOP', store=True)
    uploat_file_id = fields.Many2one('import.file.data', string='File', store=True)
