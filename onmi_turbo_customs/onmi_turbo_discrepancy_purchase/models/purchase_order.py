from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from itertools import groupby


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    check_invoices = fields.Boolean('Check invoices')

    def action_pos_discrep_purchase(self):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "onmi_turbo_discrepancy_purchase.onmi_act_pos_discrepancy_purchase")
        pos_lines = self.env['discrepancy.lines.purchase']
        for line in self.order_line:
            new_line = self.env['discrepancy.lines.purchase'].create({
                'product_id': line.product_id.id,
                'qty': 0,
                'purchase_line': line.id,
                'order_id': line.order_id.id
            })
            pos_lines |= new_line
        action['context'] = {'default_lines_id': pos_lines.ids,
                             'default_order_id': self[0].id,
                             'default_order_ids': self.ids,
                             }
        return action
    def action_neg_discrep_purchase(self):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "onmi_turbo_discrepancy_purchase.onmi_act_neg_discrepancy_purchase")
        pos_lines = self.env['discrepancy.lines.purchase']
        for line in self.order_line:
            new_line = self.env['discrepancy.lines.purchase'].create({
                'product_id': line.product_id.id,
                'qty': 0,
                'purchase_line': line.id,
                'order_id': line.order_id.id
            })
            pos_lines |= new_line
        action['context'] = {'default_lines_id': pos_lines.ids,
                             'default_order_id': self[0].id,
                             'default_order_ids': self.ids,
                             }
        return action

    def action_create_invoice_discrepancy(self):
        """Create the invoice associated to the PO WITH DISCREPANCIES.
        """

        # 1) Prepare invoice vals and clean-up the section lines
        invoice_vals_list = []
        sequence = 10
        for order in self:
            order = order.with_company(order.company_id)
            pending_section = None
            # Invoice values.
            invoice_vals = order._prepare_invoice()
            # Invoice line values (keep only necessary sections).
            for line in order.order_line:
                if line.display_type != 'line_section' and line.display_type != 'line_note':
                    line_vals = line._prepare_account_move_line()
                    line_vals.update({'sequence': sequence})
                    invoice_vals['invoice_line_ids'].append((0, 0, line_vals))
                    sequence += 1
            invoice_vals_list.append(invoice_vals)

        if not invoice_vals_list:
            raise UserError(
                _('There is no invoiceable line. If a product has a control policy based on received quantity, please make sure that a quantity has been received.'))

        # 2) group by (company_id, partner_id, currency_id) for batch creation
        new_invoice_vals_list = []
        for grouping_keys, invoices in groupby(invoice_vals_list, key=lambda x: (
        x.get('company_id'), x.get('partner_id'), x.get('currency_id'))):
            origins = set()
            payment_refs = set()
            refs = set()
            ref_invoice_vals = None
            for invoice_vals in invoices:
                if not ref_invoice_vals:
                    ref_invoice_vals = invoice_vals
                else:
                    ref_invoice_vals['invoice_line_ids'] += invoice_vals['invoice_line_ids']
                origins.add(invoice_vals['invoice_origin'])
                payment_refs.add(invoice_vals['payment_reference'])
                refs.add(invoice_vals['ref'])
            ref_invoice_vals.update({
                'ref': ', '.join(refs)[:2000],
                'invoice_origin': ', '.join(origins),
                'payment_reference': len(payment_refs) == 1 and payment_refs.pop() or False,
            })
            new_invoice_vals_list.append(ref_invoice_vals)
        invoice_vals_list = new_invoice_vals_list

        # 3) Create invoices.
        moves = self.env['account.move']
        AccountMove = self.env['account.move'].with_context(default_move_type='in_invoice')
        for vals in invoice_vals_list:
            moves |= AccountMove.with_company(vals['company_id']).create(vals)

        # 4) Some moves might actually be refunds: convert them if the total amount is negative
        # We do this after the moves have been created since we need taxes, etc. to know if the total
        # is actually negative or not
        moves.filtered(
            lambda m: m.currency_id.round(m.amount_total) < 0).action_switch_invoice_into_refund_credit_note()

        return moves
