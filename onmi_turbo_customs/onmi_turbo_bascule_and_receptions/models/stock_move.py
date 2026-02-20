from odoo import fields, models, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    waste_qty = fields.Float('Waste qty', compute='compute_waste_qty', store=False)

    def compute_waste_qty(self):
        for rec in self:
            rec.waste_qty = 0.0
            weighing = self.env['weighing'].search([('move_line_id', '=', rec.id)])
            if weighing:
                rec.waste_qty = weighing.waste