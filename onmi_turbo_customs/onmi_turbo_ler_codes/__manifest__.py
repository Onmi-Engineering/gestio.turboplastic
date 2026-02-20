{
    'name': 'TURBO LER Codes',
    'version': '18.0.0.1',
    'summary': 'ADD LER Codes to products',
    'description': 'ADD LER Codes to products',
    'category':  'ONMI developments',
    'author': 'ONMI Engineering',
    'license': 'LGPL-3',
    'depends': [
        'product',
        'stock',
        'onmi_turbo_waybill',
        'onmi_turbo_identification_document'
    ],
    'data': [
        'views/product_template_views.xml',
        'views/stock_picking_views.xml',

        'reports/report_deliveryslip.xml',
        'reports/report_waybill.xml',
        'reports/report_identification_document.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
