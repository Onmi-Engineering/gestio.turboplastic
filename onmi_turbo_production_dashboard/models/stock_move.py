from odoo import fields, models, api



class StockPicking(models.Model):
    _inherit = 'stock.move'


    
    stock_picking_partner_id = fields.Many2one(string="Producción padre",
        related="picking_id.partner_id", store=True
    )