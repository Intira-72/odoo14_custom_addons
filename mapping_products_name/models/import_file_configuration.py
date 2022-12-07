from email.policy import default
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ImportFileConfig(models.Model):
    _name = 'import.file.config'

    name = fields.Char("Name", required=True)
    im_type = fields.Selection(string="Type", selection=[('product_master_list', 'Master Lists'), ('order_lists', 'Sale Orders')], default="product_master_list")


class ImportProductMasterListFormat(models.Model):
    _name = 'import.product.master.list.format'

    