from odoo import fields, models, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    selected_bank_ids = fields.Many2many(
        'res.partner.bank',
        'account_move_bank_local_rel',
        'move_id', 'bank_id',
        string='Cuenta bancaria (factura local)',
        domain="[('partner_id', '=', company_partner_id), ('account_type', '=', 'local')]",
    )
    selected_export_bank_ids = fields.Many2many(
        'res.partner.bank',
        'account_move_bank_export_rel',
        'move_id', 'bank_id',
        string='Cuenta bancaria (factura exportación)',
        domain="[('partner_id', '=', company_partner_id), ('account_type', '=', 'export')]",
    )
    # Campo auxiliar para el dominio
    company_partner_id = fields.Many2one(
        'res.partner',
        related='company_id.partner_id',
        store=False,
    )