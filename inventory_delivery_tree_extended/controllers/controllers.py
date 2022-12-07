# -*- coding: utf-8 -*-
# from odoo import http


# class InventoryDeliveryTreeExtended(http.Controller):
#     @http.route('/inventory_delivery_tree_extended/inventory_delivery_tree_extended/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inventory_delivery_tree_extended/inventory_delivery_tree_extended/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inventory_delivery_tree_extended.listing', {
#             'root': '/inventory_delivery_tree_extended/inventory_delivery_tree_extended',
#             'objects': http.request.env['inventory_delivery_tree_extended.inventory_delivery_tree_extended'].search([]),
#         })

#     @http.route('/inventory_delivery_tree_extended/inventory_delivery_tree_extended/objects/<model("inventory_delivery_tree_extended.inventory_delivery_tree_extended"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inventory_delivery_tree_extended.object', {
#             'object': obj
#         })
