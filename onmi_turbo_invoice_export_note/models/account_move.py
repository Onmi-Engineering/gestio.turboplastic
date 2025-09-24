from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    note = fields.Text(string="note")

