# -*- coding: utf-8 -*-
{
    'name': "Custom Invoice Print",
    'summary': """Modify invoice printing format""",
    'description': """Modify invoice printing format""",
    'author': "",
    # 'website': "http://www.yourcompany.com",
    'category': 'Sales',
    'version': '0.1',
    'depends': ['base', 'sale'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
    'qweb': [
        # "static/src/xml/btn_shipping_report.xml",
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
