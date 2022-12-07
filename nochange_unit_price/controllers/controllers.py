# -*- coding: utf-8 -*-
# from odoo import http


# class NochangeUnitPrice(http.Controller):
#     @http.route('/nochange_unit_price/nochange_unit_price/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nochange_unit_price/nochange_unit_price/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nochange_unit_price.listing', {
#             'root': '/nochange_unit_price/nochange_unit_price',
#             'objects': http.request.env['nochange_unit_price.nochange_unit_price'].search([]),
#         })

#     @http.route('/nochange_unit_price/nochange_unit_price/objects/<model("nochange_unit_price.nochange_unit_price"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nochange_unit_price.object', {
#             'object': obj
#         })
