from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    total_kg = fields.Float(string="Total kg", compute="_compute_total_kg", store=True)

    @api.depends('invoice_line_ids.quantity')
    def _compute_total_kg(self):

        for rec in self:
            rec.total_kg = 0
            if rec.invoice_line_ids:
                for qty in rec.invoice_line_ids:
                    rec.total_kg += qty.quantity

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
