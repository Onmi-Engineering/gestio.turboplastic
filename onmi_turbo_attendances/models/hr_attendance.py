from odoo import fields, models, api


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    state_attendance  = fields.Selection(
        [("tocheck", "To Check"), ("revised", "Revised Turboplastic"), ("revised_v2", "Revised Adviser")],
        default="tocheck")
    
    def update_hr_attendance(self):
        for rec in self:
            rec.state_attendance  = "revised"

    def confirm_turbo(self):
          for rec in self:
            rec.state_attendance  = "revised"

    def confirm_adviser(self):
          for rec in self:
            rec.state_attendance  = "revised_v2"   

    def tocheck_turbo(self):
          for rec in self:
            rec.state_attendance  = "tocheck"             