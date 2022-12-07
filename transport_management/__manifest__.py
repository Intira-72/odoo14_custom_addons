# -*- coding: utf-8 -*-
{
    'name': "Transport Management",
    'summary': """The transport manager records transport records and generates transport documentation and confirmation of pick-up and delivery of goods from the origin and destination.""",
    'description': """The transport manager records transport records and generates transport documentation and confirmation of pick-up and delivery of goods from the origin and destination.""",
    'author': "H.Dev.",
    'category': 'Inventory',
    'version': '0.4',
    'depends': ['base', 'stock', 'contacts', 'hr', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/transport_management_view.xml',
        'views/transport_vechicles_views.xml',
        'views/transport_vechicle_types_view.xml',
        'views/btn_shipping_open_wiz.xml',
        'views/btn_report_open_wiz.xml',
        'views/assets.xml',
        'wizard/create_transport_wiz.xml',
        'wizard/transport_report_wiz.xml',
        'report/report_of_month.xml',
        'report/transport_report.xml',
        'report/report.xml',
    ],
    'demo': [],
    'qweb': [
        "static/src/xml/btn_shipping_report.xml",
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}