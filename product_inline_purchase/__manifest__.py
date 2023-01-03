# -*- coding: utf-8 -*-
{
    'name': "Product In Line (Purchase)",
    'summary': """Added display of product names on the purchase order list.""",
    'description': """Fixed a bug with retrieving the purchase price from the seller in the purchase requisition creation process.""",
    'author': "My Company",
    'category': 'purchase',
    'version': '0.2',
    'depends': ['base','purchase'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
}
