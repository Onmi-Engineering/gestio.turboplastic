{
    'name': 'TURBO Export Invoice',
    'version': '18.0.0.2',
    'summary': 'Export invoice report for Turbo Plastic',
    'description': 'Custom export invoice report with configurable header and footer',
    'category': 'ONMI developments',
    'author': 'ONMI Engineering',
    'license': 'LGPL-3',
    'depends': ['account_accountant',
                'web'],
    'data': [
        'views/base_document_layout_views.xml',
        'report/report_turbo.xml',
        'report/stock_turbo_templates.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
