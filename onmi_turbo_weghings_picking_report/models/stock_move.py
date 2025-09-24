from odoo import fields, models, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    weighing_id = fields.Many2one('weighing', compute='_compute_weighing_id')

    def _compute_weighing_id(self):
        for rec in self:
            weighing_related = self.env['weighing'].search([('move_line_id.id', '=', rec.id)])
            if weighing_related:
                for w in weighing_related:
                    rec.weighing_id = w
            else:
                rec.weighing_id = False
