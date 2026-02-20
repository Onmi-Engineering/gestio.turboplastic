from odoo import fields, models, api, _


class BaseDocumentLayout(models.TransientModel):
    _inherit = 'base.document.layout'

    company_details_waybill = fields.Html(related='company_id.company_details_waybill', readonly=False)
    report_footer_waybill = fields.Html(related='company_id.report_footer_waybill', readonly=False)
