from odoo import models, fields

class StockMove(models.Model):
    _inherit = 'stock.move'

    ler_code = fields.Char(
        string="Código LER",
        related='product_id.product_tmpl_id.ler_code',
        store=True,
        readonly=True
    )


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    ler_code = fields.Char(
        string="Código LER",
        related='product_id.product_tmpl_id.ler_code',
        store=True,
        readonly=True
    )
