# -*- coding: utf-8 -*-
# from odoo import http


# class PurchaseStateStatus(http.Controller):
#     @http.route('/purchase_state_status/purchase_state_status/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/purchase_state_status/purchase_state_status/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('purchase_state_status.listing', {
#             'root': '/purchase_state_status/purchase_state_status',
#             'objects': http.request.env['purchase_state_status.purchase_state_status'].search([]),
#         })

#     @http.route('/purchase_state_status/purchase_state_status/objects/<model("purchase_state_status.purchase_state_status"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('purchase_state_status.object', {
#             'object': obj
#         })
