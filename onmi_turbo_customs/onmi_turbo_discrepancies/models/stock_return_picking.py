from odoo import fields, models, api, _


class StockReturnPickingInherit(models.TransientModel):
    _inherit = 'stock.return.picking'

    discrep_process = fields.Boolean('Discrepancy process')
    invoice_id = fields.Many2one('account.move', string='Invoice to revert')
    invoice_ids = fields.Many2many('account.move')
    sale_id = fields.Many2one('sale.order')
    sale_ids = fields.Many2many('sale.order')
   
    def discrepancy_process(self):
       
        super(StockReturnPickingInherit, self).discrepancy_process()
        
        for sale in self.sale_id:
            sale.check_invoices = True
            sale.invoice_status = 'invoiced'

    def discrepancy_process(self):

        last_qty = self.invoice_id.invoice_line_ids[0].credit
        # 6. Return invoice and change the value of it
        invoice_reverse = self.invoice_id._reverse_moves()
        invoice_reverse = invoice_reverse.with_context(check_move_validity=False, )
        for line in invoice_reverse.invoice_line_ids:
            for lw in self.product_return_moves:
                if line.product_id == lw.product_id:
                    line.quantity = lw.quantity

        invoice_reverse.action_post()

        for sale in self.sale_ids:
            sale.check_invoices = True
            sale.invoice_status = 'invoiced'
