# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class qweb_pdf_report_example(models.Model):
#     _name = 'qweb_pdf_report_example.qweb_pdf_report_example'
#     _description = 'qweb_pdf_report_example.qweb_pdf_report_example'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
