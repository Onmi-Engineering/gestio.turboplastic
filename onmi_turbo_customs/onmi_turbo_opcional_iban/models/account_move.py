from odoo import fields, models, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    selected_bank_id = fields.Many2one(
        'res.partner.bank',
        string='Cuenta bancaria (factura local)',
        domain="[('partner_id', '=', company_partner_id), ('account_type', '=', 'local')]",
    )
    selected_export_bank_id = fields.Many2one(
        'res.partner.bank',
        string='Cuenta bancaria (factura exportación)',
        domain="[('partner_id', '=', company_partner_id), ('account_type', '=', 'export')]",
    )
    # Campo auxiliar para el dominio
    company_partner_id = fields.Many2one(
        'res.partner',
        related='company_id.partner_id',
        store=False,
    )
    selected_bank_display = fields.Char(
        compute='_compute_bank_display',
    )
    selected_export_bank_display = fields.Char(
        compute='_compute_export_bank_display',
    )

    @api.depends('selected_bank_id')
    def _compute_bank_display(self):
        for rec in self:
            bank = rec.selected_bank_id
            if bank:
                lines = [
                    bank.acc_number or '',
                    bank.bank_bic or '',
                    bank.bank_id.street or '',
                    bank.bank_id.city or '',
                    bank.bank_id.country_id.name or '',
                ]
                rec.selected_bank_display = '\n'.join(line for line in lines if line)
            else:
                rec.selected_bank_display = ''

    @api.depends('selected_export_bank_id')
    def _compute_export_bank_display(self):
        for rec in self:
            bank = rec.selected_export_bank_id
            if bank:
                lines = [
                    bank.acc_number or '',
                    bank.bank_bic or '',
                    bank.bank_id.street or '',
                    bank.bank_id.city or '',
                    bank.bank_id.country_id.name or '',
                ]
                rec.selected_export_bank_display = '\n'.join(line for line in lines if line)
            else:
                rec.selected_export_bank_display = ''