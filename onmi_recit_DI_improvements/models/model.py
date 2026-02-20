from odoo import models, fields


class IncloudRelation(models.Model):
    _inherit = 'res.partner'

    check_carrier = fields.Boolean(string='Transportista')