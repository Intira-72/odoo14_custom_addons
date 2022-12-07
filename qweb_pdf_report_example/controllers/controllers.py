# -*- coding: utf-8 -*-
# from odoo import http


# class QwebPdfReportExample(http.Controller):
#     @http.route('/qweb_pdf_report_example/qweb_pdf_report_example/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/qweb_pdf_report_example/qweb_pdf_report_example/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('qweb_pdf_report_example.listing', {
#             'root': '/qweb_pdf_report_example/qweb_pdf_report_example',
#             'objects': http.request.env['qweb_pdf_report_example.qweb_pdf_report_example'].search([]),
#         })

#     @http.route('/qweb_pdf_report_example/qweb_pdf_report_example/objects/<model("qweb_pdf_report_example.qweb_pdf_report_example"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('qweb_pdf_report_example.object', {
#             'object': obj
#         })
