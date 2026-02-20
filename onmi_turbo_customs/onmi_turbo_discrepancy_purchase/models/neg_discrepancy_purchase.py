from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
import datetime


class NegDiscrepancyPurchase(models.TransientModel):
    _name = 'neg.discrepancy.purchase'

    order_id = fields.Many2one('purchase.order')

    order_ids = fields.Many2many('purchase.order')

    lines_id = fields.Many2many('discrepancy.lines.purchase')

    def discrepancy_process(self):
        # [Facturas] Actualizar la factura con la cantidad nueva
        invoices = self.order_ids.invoice_ids
        if not invoices or len(invoices) > 1:
            raise UserError(
                _('There is no invoices created or there are more than one invoice retaled with purchase/s.\n'
                  'Please check it.'))
        if 'posted' not in invoices.state:
            invoices.action_post()
        new_inv = self.order_ids.action_create_invoice_discrepancy()
        for il in new_inv.invoice_line_ids:
            for lw in self.lines_id:
                if il.purchase_line_id.id == lw.purchase_line.id:
                    il.quantity = lw.qty
        for sale in self.order_ids:
            sale.invoice_status = 'invoiced'
        
