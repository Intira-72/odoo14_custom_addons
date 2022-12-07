# -*- coding: utf-8 -*-
{
    'name': "Products Name Mapping",
    'summary': """Associate product names within the system with different product names from multiple stores.""",
    'description': """Fixed the error unable to read the file on the server.""",
    'author': "IV",
    'category': 'product',
    'version': '0.7',
    'depends': ['base', 'stock', 'sale'],
    'data': [
        'security/ir.model.access.csv',

        'views/store.xml',
        'views/assets.xml',
        'views/product_by_stores.xml',
        'views/mapping_list_all.xml',
        'views/wrong_upload_so_list.xml',
        'views/btn_store_product_extended.xml',
        'views/btn_import_sale_order.xml',

        'wizard/open_import_update_product_list_wiz.xml',
        'wizard/import_sale_order_wiz.xml',
    ],
    'qweb': [
        "static/src/xml/btn_import_sale_order.xml",
    ],
    'demo': []
}
