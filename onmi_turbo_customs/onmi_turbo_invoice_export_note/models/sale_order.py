from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    so_total_pkg = fields.Integer(string="Total pkg", compute="_compute_total_pkg", store=True)


    @api.depends('order_line.package')
    def _compute_total_pkg(self):
        for rec in self:
            total = 0
            if rec.order_line:
                for pkg in rec.order_line:
                    try:
                        total += int(pkg.package)
                    except ValueError:
                        # Manejar el caso donde x_studio_packages no es un número válido
                        pass
            rec.so_total_pkg = total
