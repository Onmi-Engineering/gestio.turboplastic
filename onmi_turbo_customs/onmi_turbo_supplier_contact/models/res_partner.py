# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class Partner(models.Model):
    _inherit = "res.partner"

    # region Fields
    supplier_user_id = fields.Many2one('res.users', string='Supplier agent',
      help='The internal supplier agent in charge of this contact.', store=True)

    # endregion