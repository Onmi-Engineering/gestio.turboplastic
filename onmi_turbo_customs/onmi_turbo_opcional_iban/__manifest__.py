{
    'name': 'TURBO opcional iban',
    'version': '18.0.0.1',
    'summary': '',
    'description': '',
    'category': 'ONMI developments',
    'author': 'ONMI Engineering',
    'license': 'LGPL-3',
    'depends': ['base',
                'stock',
                'onmi_turbo_credit_note',],
    'data': [
        # 'views/account_move_views.xml',

        'report/external_layout_striped_template.xml',
        'report/account_move_templates.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
