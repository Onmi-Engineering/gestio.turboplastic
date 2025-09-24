from odoo import fields, models, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # region Fields DI
    treatment = fields.Char('Treatment to receive', default="R13")
    product_description = fields.Char('Product description', compute="_compute_product_description")
    gross_weight = fields.Float('Gross weight', compute="_compute_gross_weight", store=False)
    tn = fields.Char('Transfer notification')
    di_net_weight = fields.Float('Net weight', compute="_compute_di_net_weight")
    characterist = fields.Char('Remarkable features for transport and handling')
    ewl = fields.Char('E.W.L.')
    contract_treatment = fields.Char('Contract treatment')
    # endregion

    def _compute_product_description(self):
        for rec in self:
            rec.product_description = ""
            if rec.move_ids_without_package:
                for move in rec.move_ids_without_package:
                    if move.product_id:
                        rec.product_description += move.product_id.display_name + ", "

            rec.product_description = rec.product_description[:-2]

    def _compute_di_net_weight(self):
        for rec in self:
            rec.di_net_weight = 0
            if rec.weighing_ids:
                for weigh in rec.weighing_ids:
                    rec.di_net_weight += weigh.final_weight
    def _compute_gross_weight(self):
        for rec in self:
            rec.gross_weight = 0
            if rec.weighing_ids:
                for weigh in rec.weighing_ids:
                    rec.gross_weight += weigh.final_weight + weigh.waste
