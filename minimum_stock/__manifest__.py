# -*- coding: utf-8 -*-
{
    'name': "Minimum Stock Management",
    'version': "14.0.1",
    'summery': "Minimum Stock module tree views",
    'sequence': 10,
    'description': """Minimum Stock module tree views""",
    'category': "",
    'website': "",
    'depends': ['stock', 'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_minimum.xml',
        'views/assets.xml',
        'views/minimum_check_btn.xml',
    ],
    'demo': [],
    'qweb': [
        "static/src/xml/minimum_check_btn.xml",
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
