# -*- coding: utf-8 -*-
{
    'name': "Makro Order Import (XML)",
    'summary': """Upload data of sale orders list from Makro (xml file)""",
    'description': """Check Sale Order and order line for create new order line""",
    'author': "Dev",
    'website': "",
    'category': 'Sales',
    'version': '0.9.1',
    'depends': ['base', 'sale', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/makro_orders_views.xml',
        'views/makro_buyer_views.xml',
        'views/makro_store_loc.xml',
        'views/makro_products_views.xml',
        'views/makro_requisition_views.xml',
        'views/product_template_inher.xml',
        'views/btn_import_orders_wiz.xml',        
        'views/asset.xml',
        'wizard/open_import_orders.xml',
        'reports/report.xml',
    ],
    'demo': [],
    'qweb': [
        "static/src/xml/btn_makro_import_orders.xml",
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
