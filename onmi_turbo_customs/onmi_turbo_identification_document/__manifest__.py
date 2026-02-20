{
    'name': 'TURBO Identification Document',
    'version': '18.0.0.1',
    'summary': 'Identification Document PDF',
    'description': 'Identification Document PDF',
    'category':  'ONMI Developments',
    'author': 'ONMI Engineering',
    'license': 'LGPL-3',
    'depends': ['base', 'stock'],
    'data': [
        'report/stock_report_views.xml',
        'report/stock_picking_templates.xml',
        'views/res_partner_views.xml',
        'views/stock_picking_views.xml',

    ],
    'installable': True,
    'application': True,
    'auto_install': False
}