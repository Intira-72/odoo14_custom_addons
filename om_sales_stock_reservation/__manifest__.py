# -*- coding: utf-8 -*-
{
    'name': "Sales Stock Reservation",
    'summary': """""",
    'description': """""",
    'author': "IV",
    'category': '',
    'version': '0.1',
    'depends': ['base', 'sale', 'stock'],
    'data': [
        'security/ir.model.access.csv',        
        'views/res_partner_inher.xml',
        'views/sale_order_inher.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}