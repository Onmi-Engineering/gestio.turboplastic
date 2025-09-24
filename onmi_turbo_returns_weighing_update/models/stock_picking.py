from odoo import fields, models, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _action_done(self):
        res = super()._action_done()

        sale_order_lines_vals = []
        # Cambiado de self.move_lines a self.move_ids_without_package
        for move in self.move_ids_without_package:
            sale_order = move.picking_id.sale_id
            if not sale_order or move.location_dest_id.usage != 'customer' or move.sale_line_id or not move.quantity_done:
                continue
            product = move.product_id
            so_line_vals = {
                'move_ids': [(4, move.id, 0)],
                'name': product.display_name,
                'order_id': sale_order.id,
                'product_id': product.id,
                'product_uom_qty': 0,
                'qty_delivered': move.quantity_done,
                'product_uom': move.product_uom.id,
            }
            if product.invoice_policy == 'delivery':
                so_line = sale_order.order_line.filtered(lambda sol: sol.product_id == product)
                if so_line:
                    so_line_vals['price_unit'] = so_line[0].price_unit
            elif product.invoice_policy == 'order':
                so_line_vals['price_unit'] = 0
            sale_order_lines_vals.append(so_line_vals)

        if self:
            for sale_line, weighing_line in zip(self.sale_id.order_line, self.sale_id.picking_ids.weighing_ids):
                for x_weighing_line in weighing_line.sale_id.order_line:
                    if sale_line.product_id and x_weighing_line == sale_line:
                        weighing_line.final_weight = sale_line.qty_delivered
        if sale_order_lines_vals:
            self.env['sale.order.line'].with_context(skip_procurement=True).create(sale_order_lines_vals)
        return res