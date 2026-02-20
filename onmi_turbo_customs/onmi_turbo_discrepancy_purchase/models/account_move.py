from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _check_balanced(self):
        return True
