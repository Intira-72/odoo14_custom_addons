# -*- coding: utf-8 -*-
# from odoo import http


# class OmMacroOrderImportXml(http.Controller):
#     @http.route('/om_macro_order_import_xml/om_macro_order_import_xml/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/om_macro_order_import_xml/om_macro_order_import_xml/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('om_macro_order_import_xml.listing', {
#             'root': '/om_macro_order_import_xml/om_macro_order_import_xml',
#             'objects': http.request.env['om_macro_order_import_xml.om_macro_order_import_xml'].search([]),
#         })

#     @http.route('/om_macro_order_import_xml/om_macro_order_import_xml/objects/<model("om_macro_order_import_xml.om_macro_order_import_xml"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('om_macro_order_import_xml.object', {
#             'object': obj
#         })
