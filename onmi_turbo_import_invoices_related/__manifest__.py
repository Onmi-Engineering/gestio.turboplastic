{
    'name': 'TURBO Import Invoices',
    'version': '18.0.0.1',
    'summary': 'ADD import invoices related on invoices.',
    'description': 'ADD import invoices related on invoices.',
    'category':  'ONMI developments',
    'author': 'ONMI Engineering',
    'license': 'LGPL-3',
    'depends': ['account', 'payment', 'sale'],
    'data': [
        'security/ir_model_access.xml',
        'views/account_move_views.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
