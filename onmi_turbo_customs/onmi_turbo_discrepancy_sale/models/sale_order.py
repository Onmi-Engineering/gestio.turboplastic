from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def update_invoice_state(self):

        for rec in self:
                rec.invoice_status = 'invoiced'

    
                
               

        


    

