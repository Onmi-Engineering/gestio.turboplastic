{
    'name': 'TURBO Discrepancy Purchase',
    'version': '18.0.0.1',
    'summary': 'Include pos and negat discrepancies on purchase',
    'description': 'Include pos and negat discrepancies on purchase',
    'category':  'ONMI developments',
    'author': 'ONMI Engineering',
    'license': 'LGPL-3',
    'depends': ['purchase'],
    'data': [
        'security/ir_model_access.xml',
        'wizards/pos_discrepancy_purchase.xml',
        'wizards/neg_discrepancy_purchase.xml',
        'views/purchase_order_views.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
