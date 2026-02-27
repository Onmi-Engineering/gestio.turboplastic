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
            if rec.partner_id.street:
                lines.append(f"ADDRESS: {rec.partner_id.street}")
            if rec.partner_id.city:
                lines.append(f"{rec.partner_id.city}")
            if rec.partner_id.country_id.name:
                lines.append(f"{rec.partner_id.country_id.name}")
            rec.display_text = '\n'.join(lines)