# -*- coding: utf-8 -*-
{
    'name': "Inventory Disbursement Request",
    'summary': """Create documents for inventory disbursement.""",
    'description': """Create documents for inventory disbursement.""",
    'author': "H.Dev.",
    'category': 'Inventory',
    'version': '0.1',
    'depends': ['base', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/inventory_disbursement_request.xml',
        'report/requisition_report_pdf.xml',
        'report/report.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
