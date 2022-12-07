# -*- coding: utf-8 -*-
{
    'name': "Nochange Unit Price On Purchase Order",
    'summary': """There is no change in price when there is a change in the number of products on the purchase order.""",
    'description': """""",
    'author': "KPDev.",
    'category': 'Purchase',
    'version': '0.1',
    'depends': ['base', 'purchase'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
