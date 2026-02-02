from odoo import fields, models


class BaseDocumentLayout(models.TransientModel):
    _inherit = 'base.document.layout'

    company_details_export = fields.Html(
        related='company_id.company_details_export',
        readonly=False
    )
    report_footer_export = fields.Html(
        related='company_id.report_footer_export',
        readonly=False
    )
