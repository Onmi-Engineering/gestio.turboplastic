{
    'name': 'RECITOTAL Export Invoice',
    'version': '18.0.0.1',
    'summary': 'Export Invoice',
    'description': 'Export Invoice',
    'category':  'ONMI developments',
    'author': 'ONMI Engineering',
    'license': 'LGPL-3',
    'depends': ['base', 'account', 'onmi_turbo_invoice_export_note'],
    'data': [
        'views/account_move_views.xml',
        'report/report_export_invoice_document_template.xml'
        ],
    'installable': True,
    'application': True,
    'auto_install': False
}
