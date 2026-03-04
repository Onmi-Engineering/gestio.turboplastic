{
    'name': 'ONMI TURBO Weighings',
    'version': '18.0.0.1',
    'summary': 'Add in/out weighing related with transactions and sale/purchase order. Add weighings on picking reports. ',
    'description': 'Add in/out weighing related with transactions and sale/purchase order. Add weightings on picking reports.',
    'category':  'ONMI developments',
    'author': 'ONMI Engineering',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'account',
        'purchase',
        'sale',
        'stock',
    ],
    'data': [
        'security/ir_rule.xml',

        'views/license_plate_views.xml',
        'views/trailer_views.xml',
        'views/weighing_views.xml',
        'views/carriage_order_views.xml',
        'views/stock_picking_views.xml',
        'views/sale_order_views.xml',
        'views/purchase_order_views.xml',

        'views/menuitems.xml',

        'reports/stock_picking_templates.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}