from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    ler_code = fields.Char(
        string="Código LER",
        help="Código LER del residuo (introducido manualmente)"
    )
