# -*- coding: utf-8 -*-
# from odoo import http


# class MappingProductsName(http.Controller):
#     @http.route('/mapping_products_name/mapping_products_name/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mapping_products_name/mapping_products_name/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mapping_products_name.listing', {
#             'root': '/mapping_products_name/mapping_products_name',
#             'objects': http.request.env['mapping_products_name.mapping_products_name'].search([]),
#         })

#     @http.route('/mapping_products_name/mapping_products_name/objects/<model("mapping_products_name.mapping_products_name"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mapping_products_name.object', {
#             'object': obj
#         })
