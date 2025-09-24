# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, Command, fields, models

class StockMove(models.Model):
    _inherit = "stock.move"

    reported_date = fields.Datetime('Report date', compute='_compute_reported_date', store=True)

    @api.depends('picking_id.scheduled_date')
    def _compute_reported_date(self):
        for sm in self:
            if sm.picking_id:
                sm.reported_date = sm.picking_id.scheduled_date
