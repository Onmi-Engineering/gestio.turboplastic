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

    def _get_aggregated_product_quantities(self, **kwargs):
        """
        Override para incluir el código LER en las líneas agregadas
        """
        aggregated_move_lines = super()._get_aggregated_product_quantities(**kwargs)

        # Añadir código LER a cada línea agregada
        for line_key in aggregated_move_lines:
            move_line = self.filtered(lambda ml: (ml.product_id, ml.move_id.description_picking or '') == line_key[:2])
            if move_line:
                aggregated_move_lines[line_key]['ler_code'] = move_line[0].ler_code or ''

        return aggregated_move_lines
