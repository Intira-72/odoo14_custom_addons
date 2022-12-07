# -*- coding: utf-8 -*-
# from odoo import http


# class ProductInlinePurchase(http.Controller):
#     @http.route('/product_inline_purchase/product_inline_purchase/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_inline_purchase/product_inline_purchase/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_inline_purchase.listing', {
#             'root': '/product_inline_purchase/product_inline_purchase',
#             'objects': http.request.env['product_inline_purchase.product_inline_purchase'].search([]),
#         })

#     @http.route('/product_inline_purchase/product_inline_purchase/objects/<model("product_inline_purchase.product_inline_purchase"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_inline_purchase.object', {
#             'object': obj
#         })
