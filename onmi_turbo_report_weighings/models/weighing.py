from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


class Weighing(models.Model):
    _inherit = 'weighing'

    partner_picking = fields.Char('res.partner', compute='compute_partner_picking', store=True)

    date_done_picking = fields.Datetime(string="Entry date", compute="_compute_date_done_picking", store=True)

    final_weight_calculate = fields.Float('Final Weight', compute='compute_final_weight_calculate', store=True)
    company_id = fields.Many2one('res.company', compute='_compute_company_id', store=True)
    picking_state = fields.Selection(related='picking_id.state', store=True)

    def _compute_date_done_picking(self):
        for rec in self:
            if rec.picking_id:
                rec.date_done_picking = rec.picking_id.scheduled_date

    def _compute_company_id(self):
        for rec in self:
            if rec.picking_id:
                rec.company_id = rec.picking_id.company_id
            else:
                rec.company_id = False

    def compute_partner_picking(self):
        for rec in self:
            if rec.picking_id:
                rec.partner_picking = rec.picking_id.partner_id.name
            else:
                rec.partner_picking = _('not defined')

    @api.depends('first_weight', 'second_weight')
    def compute_final_weight_calculate(self):
        for rec in self:
            rec.final_weight_calculate = 0.0
            if rec.first_weight and rec.second_weight:
                if rec.first_weight > 0.0 and rec.second_weight > 0.0:
                    # Come from SALE ORDERS
                    if rec.type == 'output':
                        if rec.first_weight > rec.second_weight:
                            raise ValidationError(
                                _('First Weight can´t be upper than second one on Weighings from Sale Orders.\n'
                                  'Please, check this value for the correct calculation.\n'))
                        rec.final_weight_calculate = rec.second_weight - rec.first_weight - rec.waste

                    # Come from PURCHASE ORDERS
                    if rec.type == 'input':
                        if rec.first_weight < rec.second_weight:
                            raise ValidationError(
                                _('Second Weight can´t be upper than first one on Weighings from Purchase Orders.\n'
                                  'Please, check these values for the correct calculation.\n'))
                        rec.final_weight_calculate = rec.first_weight - rec.second_weight - rec.waste
