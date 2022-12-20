# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MakroOrders(models.Model):
    _name = 'om_makro_order_import_xml.makro_orders'
    _description = 'om_makro_order_import_xml.makro_orders'

    name = fields.Char("File Name")
   