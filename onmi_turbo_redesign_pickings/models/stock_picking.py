from odoo import fields, models, api, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    delivery_service = fields.Boolean('Delivery Service')
