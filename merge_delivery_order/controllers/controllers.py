# -*- coding: utf-8 -*-
# from odoo import http


# class MergeDeliveryOrder(http.Controller):
#     @http.route('/merge_delivery_order/merge_delivery_order/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/merge_delivery_order/merge_delivery_order/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('merge_delivery_order.listing', {
#             'root': '/merge_delivery_order/merge_delivery_order',
#             'objects': http.request.env['merge_delivery_order.merge_delivery_order'].search([]),
#         })

#     @http.route('/merge_delivery_order/merge_delivery_order/objects/<model("merge_delivery_order.merge_delivery_order"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('merge_delivery_order.object', {
#             'object': obj
#         })
