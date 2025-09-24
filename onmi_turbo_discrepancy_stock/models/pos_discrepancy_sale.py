from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


class PosDiscrepancySale(models.TransientModel):
    _name = 'pos.discrepancy.sale'

    order_id = fields.Many2one('sale.order')

    order_ids = fields.Many2many('sale.order')

    lines_id = fields.Many2many('discrepancy.lines')

    def discrepancy_process(self):
        if not self.order_ids.invoice_ids or (
                self.order_ids.invoice_ids and 'posted' not in self.order_ids.invoice_ids.state):
            raise UserError(_("There is not posted invoices on this sale order"))

        # [Facturas] Crear una factura con la cantidad nueva
        new_inv = self.order_ids.create_invoice_discrep()
        new_inv = new_inv.with_context(check_move_validity=False, )
        for il in new_inv.invoice_line_ids:
            for lw in self.lines_id:
                if lw.order_line.id in il.sale_line_ids.ids:
                    il.quantity = lw.qty
        new_inv.action_post()
        for order in self.order_ids:
            order.check_invoices = True
            order.invoice_status = 'invoiced'
