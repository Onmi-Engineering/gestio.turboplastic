{
    'name': 'ONMI TURBO Discrepancies',
    'version': '18.0.0.1',
    'summary': 'Sales, purchases and stock discrepancies',
    'description': 'Include pos and negat discrepancies on purchase. discrepancy sale. Make moves from sales or purchases.',
    'category':  'ONMI developments',
    'author': 'ONMI Engineering',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'account',
        'purchase',
        'sale',
        'stock'
    ],
    'data': [
        'security/ir_model_access.xml',

        'views/neg_discrepancy_purchase.xml',
        'views/pos_discrepancy_purchase.xml',
        'views/pos_discrepancy_sale_views.xml',
        'views/stock_return_picking_views.xml',

        'views/purchase_order_views.xml',
        'views/sale_order_views.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False
}
