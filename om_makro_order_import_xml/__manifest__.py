# -*- coding: utf-8 -*-
{
    'name': "Makro Order Import (XML)",
    'summary': """Upload data of sale orders list from Makro (xml file)""",
    'description': """Add Search Views""",
    'author': "Dev",
    'website': "",
    'category': 'Sales',
    'version': '0.2',
    'depends': ['base', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/makro_orders_views.xml',
        'views/makro_buyer_views.xml',
        'views/makro_store_loc.xml',
        'views/makro_products_views.xml',
        'views/btn_import_orders_wiz.xml',
        'views/asset.xml',
        'wizard/open_import_orders.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'qweb': [
        "static/src/xml/btn_makro_import_orders.xml",
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
