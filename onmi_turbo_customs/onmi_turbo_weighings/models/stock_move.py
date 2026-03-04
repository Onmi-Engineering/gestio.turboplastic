from odoo import fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    code_led = fields.Char(string="L.E.R")
    weighing_id = fields.Many2one('weighing', compute='_compute_weighing_id')
    waste_qty = fields.Float('Waste qty', compute='compute_waste_qty', store=False)

    def _compute_weighing_id(self):
        for rec in self:
            weighing_related = self.env['weighing'].search([('move_line_id.id', '=', rec.id)])
            if weighing_related:
                for w in weighing_related:
                    rec.weighing_id = w
            else:
                rec.weighing_id = False

    def compute_waste_qty(self):
        for rec in self:
            rec.waste_qty = 0.0
            weighing = self.env['weighing'].search([('move_line_id', '=', rec.id)])
            if weighing:
                rec.waste_qty = weighing.waste