# -*- coding: utf-8 -*-
{
    'name': "Inventory Turnovers Analysis Report",
    'summary': """Calculating inventory turnover.""",
    'description': """""",
    'author': "IV",
    'category': '',
    'version': '0.1',
    'depends': ['base', 'stock', 'product', 'purchase', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        
        # 'views/estate_property_offer_views.xml',
        # 'views/estate_property_views.xml',
        # 'views/estate_property_type_views.xml',
        # 'views/estate_property_tag_views.xml',        

        'wizard/inventory_turnover_report_wiz.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}