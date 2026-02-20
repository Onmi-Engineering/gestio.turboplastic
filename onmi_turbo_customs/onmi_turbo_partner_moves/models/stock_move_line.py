from odoo import fields, models, api, _


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    partner_picking_id = fields.Many2one('res.partner', compute='_compute_partner_picking_id', store=True)

    def _compute_partner_picking_id(self):
        for rec in self:
            if rec.picking_id:
                rec.partner_picking_id = rec.picking_id.partner_id
