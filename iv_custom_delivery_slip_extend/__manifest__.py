{
    'name': 'Custom Delivery Slip',
    'version': '3.0',
    'description': 'Add Destination Location to Form',
    'summary': '',
    'author': 'In.V',
    'website': '',
    'license': 'LGPL-3',
    'category': 'Inventory',
    'depends': [
        'base', 'stock'
    ],
    'data': [
        # 'views/stock_move_line_views.xml',

        'report/report_deliveryslip_template.xml',
    ],
    'demo': [
        ''
    ],
    'auto_install': False,
    'application': True,
}