from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    company_details_export = fields.Html(
        string='Company Details Export Invoice',
        help="Header text displayed at the top of export invoice report."
    )
    report_footer_export = fields.Html(
        string='Report Footer Export Invoice',
        translate=True,
        help="Footer text displayed at the bottom of export invoice report."
    )
