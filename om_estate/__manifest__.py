# -*- coding: utf-8 -*-
{
    'name': "Real Estate",
    'summary': """""",
    'description': """""",
    'author': "IV",
    'category': '',
    'version': '0.1',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',  
        'views/estate_user_view_inher.xml',      

        'views/estate_menus.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}