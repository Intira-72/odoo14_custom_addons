# -*- coding: utf-8 -*-
{
    'name': "Qweb PDF Report Example",
    'summary': """Qweb PDF Report Example""",
    'description': """""",
    'author': "My Company",
    'category': 'School',
    'version': '0.1',
    'depends': ['base', 'school', 'school_student'],
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'report/student_report_template.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
