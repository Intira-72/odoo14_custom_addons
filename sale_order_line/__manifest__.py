# -*- coding: utf-8 -*-

{
    'name': 'Sale Order Lines',
    'version': '14.0',
    'author': 'H.Dev.',
    'category': 'sale',
    'description': """Enhancement in sale module""",
    'depends': ['base','sale_management','sale','stock_account'],
    'license': 'LGPL-3',
    'data': [
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
