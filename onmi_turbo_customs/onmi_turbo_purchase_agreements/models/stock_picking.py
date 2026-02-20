from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    
    product_qty_total = fields.Float(compute="calculate_product_qty_waste")
    

    def calculate_product_qty_waste(self):
      
     for rec in self:
           rec.product_qty_total = 0.0
           for li in rec.purchase_id.order_line:    
                rec.product_qty_total += li.product_qty
         

          

     
