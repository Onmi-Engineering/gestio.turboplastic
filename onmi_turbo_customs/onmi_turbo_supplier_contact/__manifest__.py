{
    'name': 'TURBO Supplier Contacts',
    'version': '18.0',
    'summary': 'Include internal user from clients and restrict permissions on these internal users',
    'description': "Include internal user from clients and restrict permissions on these internal users",
    'license': 'LGPL-3',
    'depends': ['account', 'contacts', 'purchase', 'purchase_own_documents'],
    'category': '',
    'data': [
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}