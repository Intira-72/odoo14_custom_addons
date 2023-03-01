# -*- coding: utf-8 -*-
{
    'name': "Packing Process Management",
    'summary': """""",
    'description': """""",
    'author': "IV",
    'category': '',
    'version': '0.1',
    'depends': ['base', 'stock', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        
        'views/packing_views.xml',
        'views/packing_teams_views.xml',
        # 'views/estate_property_tag_views.xml',
        # 'views/estate_property_offer_views.xml',

        'views/packing_menus.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}