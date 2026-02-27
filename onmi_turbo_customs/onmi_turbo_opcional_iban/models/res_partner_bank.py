from odoo import fields, models, api

class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    account_type = fields.Selection(
        string='Tipo de facturas',
        selection=[
            ('local', 'Factura local'),
            ('export', 'Factura exportación'),
        ]
    )

    display_text = fields.Char(
        string='Texto bancario',
        compute='_compute_display_text',
    )

    @api.depends('acc_number', 'bank_bic', 'partner_id.street', 'partner_id.city', 'partner_id.country_id')
    def _compute_display_text(self):
        for rec in self:
            lines = []
            if rec.bank_id.name:
                lines.append(f"BANK: {rec.bank_id.name}")
            if rec.acc_number:
                lines.append(f"EURO ACCOUNT: {rec.acc_number}")
            if rec.bank_bic:
                lines.append(f"BIC: {rec.bank_bic}")
            if rec.bank_id.street:
                lines.append(f"ADDRESS: {rec.bank_id.street}, {rec.bank_id.street2 or ''}, {rec.bank_id.zip or ''}")
            if rec.bank_id.city and rec.bank_id.country.name:
                lines.append(f"{rec.bank_id.city}, {rec.bank_id.country.name}")
            rec.display_text = '\n'.join(lines)