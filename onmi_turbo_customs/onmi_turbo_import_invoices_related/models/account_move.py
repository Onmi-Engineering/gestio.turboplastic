from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    invoice_related_ids = fields.Many2many('account.move.related')
