{
    'name': 'TURBO Attendances',
    'version': '18.0.0.1',
    'summary': 'Attendances',
    'description': 'Attendances',
    'category':  'ONMI developments',
    'author': 'ONMI Engineering',
    'license': 'LGPL-3',
    'depends': ['base', 'hr', 'calendar', 'account'],
    'data': [
        'security/security.xml',
        'views/hr_attendance_views.xml',
        'views/hr_employee_view.xml'
        ],
    'installable': True,
    'application': True,
    'auto_install': False
}
