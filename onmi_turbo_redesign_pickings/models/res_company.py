from odoo import fields, models, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    company_details_picking = fields.Html(string='Company Details Picking',
                                          help="Header text displayed at the top of picking report.")
    report_footer_picking = fields.Html(string='Report Footer Picking', translate=True,
                                help="Footer text displayed at the bottom of of picking report.")
