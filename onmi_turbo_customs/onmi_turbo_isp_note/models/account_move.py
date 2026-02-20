from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    has_isp = fields.Boolean(string='Has ISP', compute='_compute_has_isp', default=False, store=False)

    def _compute_has_isp(self):
        for rec in self:
            taxes_lines = rec.invoice_line_ids.tax_ids
            rec.has_isp = False
            for tl in taxes_lines:
               if  tl.l10n_es_type:
                if 'sujeto_isp' in tl.l10n_es_type:
                    rec.has_isp = True
                    break   
                
                    

