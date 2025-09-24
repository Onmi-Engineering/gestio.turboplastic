from odoo import fields, models, api, _


class StockReturnPickingInherit(models.TransientModel):
    _inherit = 'stock.return.picking'

   
    def discrepancy_process(self):
       
        super(StockReturnPickingInherit, self).discrepancy_process()
        
        for sale in self.sale_id:
            sale.check_invoices = True
            sale.invoice_status = 'invoiced'
        
           
