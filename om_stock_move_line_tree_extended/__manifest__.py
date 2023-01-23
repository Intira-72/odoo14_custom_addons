# -*- coding: utf-8 -*-
{
    'name': "Stock Move Views Extended",
    'version': "14.0.1",
    'summery': "Add Source Document on tree views",
    'sequence': 10,
    'description': """Add Source Document on tree views""",
    'category': "Inventory",
    'website': "",
    'license': "LGPL-3",
    'depends': ['base', 'stock'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/view_move_line_tree_ex.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
