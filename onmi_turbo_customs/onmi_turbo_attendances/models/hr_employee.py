from odoo import api, fields, models, _

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    affiliation_number_id = fields.Char('Nº Affiliation')
    date_old = fields.Date('Date old')
          
      
    