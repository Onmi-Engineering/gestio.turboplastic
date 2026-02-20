from odoo import fields, models, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    company_details_waybill = fields.Html(string='Company Details Waybill',
                                          help="Header text displayed at the top of Waybill report.")
    report_footer_waybill = fields.Html(string='Report Footer Waybill', translate=True,
                                help="Footer text displayed at the bottom of Waybill report.")

    stamp = fields.Binary("Stamp")
