{
    'name': 'RECITOTAL DI improvement',
    'version': '18.0.0.1',
    'summary': 'DI improvement',
    'description': 'DI improvement',
    'category':  'ONMI developments',
    'author': 'ONMI Engineering',
    'license': 'LGPL-3',
    'depends': ['base', 'onmi_turbo_identification_document', 'stock'],
    'data': [
        'views/stock_picking_views.xml',
        'views/res_partner_views.xml',
        'report/report_invoice_document_template.xml'
        ],
    'installable': True,
    'application': True,
    'auto_install': False
}
