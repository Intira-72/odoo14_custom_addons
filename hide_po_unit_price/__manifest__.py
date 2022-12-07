# -*- coding: utf-8 -*-
{
    'name': "Hide PO Unit Price For Purchase User Receipts",
    'summary': """Grant the right to accept the item from the order list but can't see the price per piece. (can see purchase order but turn off price visibility)""",
    'description': """Grant the right to accept the item from the order list but can't see the price per piece. (can see purchase order but turn off price visibility)""",
    'author': "In.V",
    'category': 'Purchase',
    'version': '0.1',
    'depends': ['base', 'purchase'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/purchase_order_form_inherit.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}