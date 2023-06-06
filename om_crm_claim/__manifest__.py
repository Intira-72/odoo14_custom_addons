# -*- coding: utf-8 -*-
{
    'name': "CRM Claim Management",
    'summary': """""",
    'description': """""",
    'author': "IV",
    'category': 'Sale',
    'version': '0.1',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',        
        
        'views/crm_claim_views.xml',
        'views/crm_claim_menus.xml',
        # 'views/estate_property_type_views.xml',
        # 'views/estate_property_tag_views.xml',  
        # 'views/estate_user_view_inher.xml',      

        # 'views/estate_menus.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}