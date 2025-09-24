from odoo import fields, models, api


class AccountEdiDocument(models.Model):
    _inherit = 'account.edi.document'

    @api.model
    def _cron_process_documents_web_services(self, job_count=None):
        '''OVERRIDE'''
        ''' Method called by the EDI cron processing all web-services.

        :param job_count: Limit explicitely the number of web service calls. If not provided, process all.
        '''
        edi_documents = self.search([('state', 'in', ('to_send', 'to_cancel'))])
        # nb_remaining_jobs = edi_documents._process_documents_web_services(job_count=job_count)
        edi_documents._process_documents_web_services(job_count=job_count)
        # Mark the CRON to be triggered again asap since there is some remaining jobs to process.
        # if nb_remaining_jobs > 0:
        #     self.env.ref('account_edi.ir_cron_edi_network')._trigger()

