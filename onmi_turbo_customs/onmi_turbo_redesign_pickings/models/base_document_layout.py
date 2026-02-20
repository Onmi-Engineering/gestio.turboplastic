from odoo import fields, models, api


class BaseDocumentLayout(models.TransientModel):
    _inherit = 'base.document.layout'


    company_details_picking = fields.Html(related='company_id.company_details_picking', readonly=False)
    report_footer_picking = fields.Html(related='company_id.report_footer_picking', readonly=False)

