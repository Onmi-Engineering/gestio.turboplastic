# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _



class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        for po in self:
            if po.partner_id and po.partner_id.supplier_user_id:
                po.user_id = po.partner_id.supplier_user_id