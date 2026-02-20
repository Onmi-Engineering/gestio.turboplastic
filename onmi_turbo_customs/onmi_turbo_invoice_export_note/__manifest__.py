{
    'name': 'ONMI Turbo invoice export note',
    'version': '18.0.0.1',
    'summary': 'Add a note on the page exportacion.',
    'description': 'ONMI Turbo invoice export note',
    'category':  'ONMI developments',
    'author': 'ONMI Engineering',
    'license': 'LGPL-3',
    'depends': ['stock', 'sale', 'onmi_turbo_credit_note'],
    'data': [
    'views/account_move_views.xml',
    'report/invoice_exportacion.xml',
    'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
