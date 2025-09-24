from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    nima = fields.Char('NIMA')
    cnae = fields.Char('C.N.A.E.', default="3811/3812")
    rpgr = fields.Char('RPGR')
    document_user_id = fields.Many2one('res.partner')
    operator_type = fields.Selection([
        ('producer', 'Producer'),
        ('manager', 'Manager'),
        ('last_manager', 'Last Manager')],
        string='Operator Type', )
