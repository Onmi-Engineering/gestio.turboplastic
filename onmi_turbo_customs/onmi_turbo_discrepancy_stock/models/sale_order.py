from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    check_invoices = fields.Boolean('Check invoices')

    def action_dicrepancy_sale_order(self):
        if not self.invoice_ids or not any(invoice.state == 'posted' for invoice in self.invoice_ids):
        # if not self.invoice_ids or (self.invoice_ids and 'posted' not in self.invoice_ids.state):
            raise UserError(_("There is not posted invoices on this sale order"))
        action = self.env["ir.actions.actions"]._for_xml_id(
            "onmi_turbo_discrepancy_stock.onmi_act_stock_return_picking")
        action['context'] = {'default_picking_id': self.picking_ids[0].id,
                             'default_discrep_process': True,
                             'default_sale_id': self.id,
                             'default_invoice_id': self.invoice_ids[0].id,
                             'default_invoice_ids': self.invoice_ids.ids}
        return action

    def action_dicrepancy_sale_order_massive(self):
        if not self.invoice_ids or (self.invoice_ids and 'posted' not in self.invoice_ids.state):
            raise UserError(_("There is not posted invoices on this sale order"))
        action = self.env["ir.actions.actions"]._for_xml_id(
            "onmi_turbo_discrepancy_stock.onmi_act_stock_return_picking")
        action['context'] = {'default_picking_id': self.picking_ids[0].id,
                             'default_discrep_process': True,
                             'default_sale_ids': self.ids,
                             'default_invoice_id': self.invoice_ids[0].id,
                             'default_invoice_ids': self.invoice_ids.ids}
        return action

    def action_positive_dicrepancy_sale_order(self):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "onmi_turbo_discrepancy_stock.onmi_act_pos_discrepancy_sale")
        pos_lines = self.env['discrepancy.lines']
        for line in self.order_line:
            new_line = self.env['discrepancy.lines'].create({
                'product_id': line.product_id.id,
                'qty': 0,
                'order_line': line.id,
                'order_id': line.order_id.id
            })
            pos_lines |= new_line
        action['context'] = {'default_lines_id': pos_lines.ids,
                             'default_order_id': self[0].id,
                             'default_order_ids': self.ids}
        return action

    def _get_invoiceable_lines_discrep(self, final=False):
        """Return the invoiceable lines for order `self`."""
        down_payment_line_ids = []
        invoiceable_line_ids = []
        pending_section = None
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')

        for line in self.order_line:
            if line.display_type != 'line_section' and line.display_type != 'line_note':
                invoiceable_line_ids.append(line.id)

        return self.env['sale.order.line'].browse(invoiceable_line_ids)

    def create_invoice_discrep(self):
        invoice_vals_list = []
        invoice_item_sequence = 0  # Incremental sequencing to keep the lines order on the invoice.
        for order in self:
            order = order.with_company(order.company_id)
            current_section_vals = None
            down_payments = order.env['sale.order.line']

            invoice_vals = order._prepare_invoice()
            invoiceable_lines = order._get_invoiceable_lines_discrep(False)

            if not any(not line.display_type for line in invoiceable_lines):
                continue

            invoice_line_vals = []
            down_payment_section_added = False
            for line in invoiceable_lines:
                if not down_payment_section_added and line.is_downpayment:
                    # Create a dedicated section for the down payments
                    # (put at the end of the invoiceable_lines)
                    invoice_line_vals.append(
                        (0, 0, order._prepare_down_payment_section_line(
                            sequence=invoice_item_sequence,
                        )),
                    )
                    down_payment_section_added = True
                    invoice_item_sequence += 1
                invoice_line_vals.append(
                    (0, 0, line._prepare_invoice_line(
                        sequence=invoice_item_sequence,
                    )),
                )
                invoice_item_sequence += 1

            invoice_vals['invoice_line_ids'] += invoice_line_vals
            invoice_vals_list.append(invoice_vals)

        moves = self.env['account.move'].sudo().with_context(default_move_type='out_invoice').create(
            invoice_vals_list)

        return moves
