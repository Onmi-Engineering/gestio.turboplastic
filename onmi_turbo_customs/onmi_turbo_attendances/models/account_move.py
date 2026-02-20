from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    total_pkg = fields.Float(string="Total Packages", compute="_compute_total_pkg", store=True)

    @api.depends('invoice_line_ids.x_studio_packages')
    def _compute_total_pkg(self):
        for rec in self:
            total = 0
            if rec.invoice_line_ids:
                for pkg in rec.invoice_line_ids:
                    try:
                        total += int(pkg.x_studio_packages)
                    except ValueError:
                        # Manejar el caso donde x_studio_packages no es un número válido
                        pass
            rec.total_pkg = total
