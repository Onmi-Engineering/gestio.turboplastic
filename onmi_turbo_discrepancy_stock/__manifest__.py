{
    'name': 'TURBO Discrepancy Sale',
    'version': '18.0.0.1',
    'summary': 'Make moves from sales or purchases.',
    'description': 'Make moves from sales or purchases.',
    'category':  'ONMI develpments',
    'author': 'ONMI Engineering',
    'license': 'LGPL-3',
    'depends': ['sale', 'purchase'],
    'data': [
        'security/ir_rule.xml',
        # 'views/sale_order_views.xml', #Se elimina por peticion del cliente pero queda por si lo vuelven a solicitar
        'wizard/pos_discrepancy_sale_views.xml',
        # 'wizard/stock_return_picking_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
