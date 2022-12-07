# -*- coding: utf-8 -*-
{
    'name': "Custom Sale Tree View",
    'summary': """To customize the display of the list Sale Quotations""",
    'description': """To customize the display of the list Sale Quotations""",
    'author': "My Company",
    'category': 'Sale',
    'version': '0.1',
    'depends': ['base', 'sale'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
