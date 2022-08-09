# -*- coding: utf-8 -*-
{
    'name': "User’s Own Forms/ Documents Only (Odoo Purchase Module)",
    'summary': "User’s Own Forms/ Documents Only (Odoo Purchase Module)",
    'author': "iTech Resources",
    'website': "https://itechresources.pk",
    'license': 'LGPL-3',
    "installable": True,
    'auto_install': False,
    'price': '4.43',
    'currency': 'EUR',
    'category': 'Purchase',
    'version': '15.0',


    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'purchase','crm','purchase_own_documents'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/po_own_documents.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    'images': ['static/description/banner.gif'],
    'application': False,
}
