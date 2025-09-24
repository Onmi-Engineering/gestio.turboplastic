from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
import datetime


class PosDiscrepancyPurchase(models.TransientModel):
    _name = 'pos.discrepancy.purchase'

    order_id = fields.Many2one('purchase.order')

    order_ids = fields.Many2many('purchase.order')

    lines_id = fields.Many2many('discrepancy.lines.purchase')

    def discrepancy_process(self):
        # Return invoice and change the value of it
        invoices = self.order_ids.invoice_ids
        if not invoices or len(invoices) > 1:
            raise UserError(
                _('There is no invoices created or there are more than one invoice retaled with purchase/s.\n'
                  'Please check it.'))
        if 'posted' in invoices.state:
            raise UserError(
                _('You can process a negative discrepancy with a invoice confirmed, invoice: %s', invoices.name))
        for il in invoices.invoice_line_ids:
            for lw in self.lines_id:
                if il.purchase_line_id.id == lw.purchase_line.id:
                    il.quantity -= lw.qty
        self.order_ids.check_invoices = True
