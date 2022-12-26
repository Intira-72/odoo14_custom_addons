# -*- coding: utf-8 -*-
{
    'name': "Inventory Delivery Extended",

    'summary': """adjust the settings of the delivery list display page.""",

    'description': """
        adjust the settings of the delivery list display page.
    """,
    'author': "H.Dev",
    'category': 'Inventory',
    'version': '0.4',
    'depends': ['base', 'stock', 'sale', 'purchase'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/stock_picking_extended.xml',
        # 'views/templates.xml',
    ],
}
