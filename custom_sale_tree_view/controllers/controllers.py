# -*- coding: utf-8 -*-
# from odoo import http


# class CustomSaleTreeView(http.Controller):
#     @http.route('/custom_sale_tree_view/custom_sale_tree_view/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_sale_tree_view/custom_sale_tree_view/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_sale_tree_view.listing', {
#             'root': '/custom_sale_tree_view/custom_sale_tree_view',
#             'objects': http.request.env['custom_sale_tree_view.custom_sale_tree_view'].search([]),
#         })

#     @http.route('/custom_sale_tree_view/custom_sale_tree_view/objects/<model("custom_sale_tree_view.custom_sale_tree_view"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_sale_tree_view.object', {
#             'object': obj
#         })
