from odoo import fields, models, api, _


class AccountMoveRelated(models.Model):
    _name = 'account.move.related'

    invoice_id = fields.Many2one('account.move')
    name = fields.Char(related="invoice_id.name")
