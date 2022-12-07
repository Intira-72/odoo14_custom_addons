# -*- coding: utf-8 -*-
# from odoo import http


# class InventoryDisbursementRequest(http.Controller):
#     @http.route('/inventory_disbursement_request/inventory_disbursement_request/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inventory_disbursement_request/inventory_disbursement_request/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inventory_disbursement_request.listing', {
#             'root': '/inventory_disbursement_request/inventory_disbursement_request',
#             'objects': http.request.env['inventory_disbursement_request.inventory_disbursement_request'].search([]),
#         })

#     @http.route('/inventory_disbursement_request/inventory_disbursement_request/objects/<model("inventory_disbursement_request.inventory_disbursement_request"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inventory_disbursement_request.object', {
#             'object': obj
#         })
