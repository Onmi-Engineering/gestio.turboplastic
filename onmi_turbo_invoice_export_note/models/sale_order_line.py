from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    package = fields.Char(string="Package")
    container = fields.Char(string="Container")
    seal = fields.Char(string="Seal No")
    package_type = fields.Selection([("bl1", "Bales"), ("bl2", "Bigbag"), ("bl3", "Packages")])


    def _prepare_invoice_line(self, **optional_values):
        # Llamar a la implementación original de la función
        res = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)

        # Añadir los nuevos campos personalizados al diccionario resultante
        res.update({
            'x_studio_packages': self.package,
            'x_studio_container_no': self.container,
            'x_studio_seal_no': self.seal,
            'x_studio_gross_weight': self.product_uom_qty,
            'inv_package_type': self.package_type,
        })

        return res
