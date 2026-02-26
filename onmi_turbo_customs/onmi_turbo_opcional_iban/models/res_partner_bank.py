from odoo import fields, models

class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    account_type = fields.Selection(
        string='Cuenta para facturas locales / de exportación',
        selection=[
            ('local', 'Factura local'),
            ('export', 'Factura exportación'),
        ]
    )