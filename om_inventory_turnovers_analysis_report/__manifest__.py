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
        
        'wizard/inventory_turnover_report_wiz.xml',
        'report/report.xml',
        'report/inventory_turnover_pdf_report.xml',
        # 'report/inventory_turnover_xlsx_report.xml',       
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}