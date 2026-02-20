{
    'name': 'TURBO Waybill',
    'version': '18.0.0.1',
    'summary': 'PDF Carta de Porte',
    'description': 'PDF Carta de Porte ',
    'category':  'ONMI develpments',
    'author': 'ONMI Engineering',
    'license': 'LGPL-3',
    'depends': ['stock'],
    'data': [
        'report/stock_picking_templates.xml',
        'report/stock_report_views.xml',
        'views/base_document_layout_views.xml',
        'views/stock_picking_views.xml',
        'views/res_company_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
