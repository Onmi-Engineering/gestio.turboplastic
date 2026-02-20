from datetime import timedelta, datetime, date
import calendar
from odoo import fields, models, api, _


class weighing(models.Model):
    _inherit = 'weighing'

   
    code_led = fields.Char(string="L.E.R")
    description = fields.Text(        
        'Description', compute='compute_final_descripcion')
    
    
    def compute_final_descripcion(self):    

        for rec in self:
            sale = rec.move_line_id.sale_line_id    
            purchase =  rec.move_line_id.purchase_line_id
            rec.description = False                                 
            if  rec.sale_id.order_line:
              for line in rec.sale_id.order_line:                   
                    if line.product_id:                        
                            if line ==  sale:                                                             
                                if line.name != line.product_id.name and line.name != line.product_id.display_name:
                                 rec.description = line.name
            if  rec.purchase_id.order_line:
             for li in rec.purchase_id.order_line:                   
                    if li.product_id:              
                            if li ==  purchase:                             
                                if li.name != li.product_id.name and li.name != li.product_id.display_name:
                                 rec.description = li.name
              



                                      

                                
            



