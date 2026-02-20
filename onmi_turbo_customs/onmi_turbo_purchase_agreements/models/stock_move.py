import base64
from odoo import api, fields, models, _


class StockMove(models.Model):
    _inherit = 'stock.move'

    
    
    product_qty_picking = fields.Float(compute="calculate_product_qty_waste")
    name_purchase = fields.Char(compute="calculate_name_purchase")
    product_qty_total = fields.Float(compute="calculate_product_qty")
    

    def calculate_product_qty_waste(self):

        for rec in self:
            rec.product_qty_picking = 0
            if rec.purchase_line_id:          
                  rec.product_qty_picking = rec.purchase_line_id.product_qty  

    def calculate_name_purchase(self):

        for rec in self:
            if rec.purchase_line_id:          
                  rec.name_purchase = rec.purchase_line_id.product_id  

    def calculate_product_qty(self):
         
        for rec in self:
            rec.product_qty_total = 0
            if rec.purchase_line_id:          
                  rec.product_qty_total += rec.purchase_line_id.product_qty                                    
                