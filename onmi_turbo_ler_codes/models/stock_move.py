from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)

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
            # Obtener el producto desde el diccionario ya generado
            product = aggregated_move_lines[line_key].get('product')

            if product and product.product_tmpl_id:
                aggregated_move_lines[line_key]['ler_code'] = product.product_tmpl_id.ler_code or ''
            else:
                aggregated_move_lines[line_key]['ler_code'] = ''

        return aggregated_move_lines