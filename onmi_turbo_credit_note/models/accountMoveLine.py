from odoo import fields, models, api


class accountMoveLine(models.Model):
    _inherit = 'account.move.line'

    inverse_subtotal = fields.Float(compute = 'compute_inverse',default = 0)
    
    def compute_inverse(self):
     
        for linea in self:
              
                linea.inverse_subtotal =  linea.price_subtotal * (-1)


    

                
             
        
   

