# -*- coding: utf-8 -*-
# from odoo import http


# class OmCustomInvoicePrint(http.Controller):
#     @http.route('/om_custom_invoice_print/om_custom_invoice_print/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/om_custom_invoice_print/om_custom_invoice_print/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('om_custom_invoice_print.listing', {
#             'root': '/om_custom_invoice_print/om_custom_invoice_print',
#             'objects': http.request.env['om_custom_invoice_print.om_custom_invoice_print'].search([]),
#         })

#     @http.route('/om_custom_invoice_print/om_custom_invoice_print/objects/<model("om_custom_invoice_print.om_custom_invoice_print"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('om_custom_invoice_print.object', {
#             'object': obj
#         })
