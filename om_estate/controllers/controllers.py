# -*- coding: utf-8 -*-
# from odoo import http


# class OmEstate(http.Controller):
#     @http.route('/om_estate/om_estate/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/om_estate/om_estate/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('om_estate.listing', {
#             'root': '/om_estate/om_estate',
#             'objects': http.request.env['om_estate.om_estate'].search([]),
#         })

#     @http.route('/om_estate/om_estate/objects/<model("om_estate.om_estate"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('om_estate.object', {
#             'object': obj
#         })
