from odoo import fields, models, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    inv_package_type = fields.Selection(
        selection=[("bl1", "Bales"), ("bl2", "Bigbag"), ("bl3", "Packages")],
        string="Package Type",
        store=True,
        copy=True,  # This ensures the value is copied when duplicating records
    )

    # This ensures the field is included in the create/write operations
    @api.model
    def _add_missing_default_values(self, values):
        values = super()._add_missing_default_values(values)
        if 'inv_package_type' not in values:
            values['inv_package_type'] = False
        return values