
from odoo import models, fields, api

class incloud_relation(models.Model):
    _inherit = 'res.partner'
    
    check_carrier = fields.Boolean(string='Transportista')
    
    