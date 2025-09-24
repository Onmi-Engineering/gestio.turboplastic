from odoo import fields, models, api
import json


class accountMoveTaxe(models.Model):
    _inherit = 'account.move'
       
    inverse_total_taxes = fields.Float(compute = 'compute_taxes',default = 0)
    inverse_total_untaxes = fields.Float(compute = 'compute_untaxes',default = 0)   
    inverse_tax_totals_json = fields.Char(
        string="Invoice Totals JSON",
        compute='_compute_inverse_tax_totals_json',
        readonly=False,
        help='Edit Tax amounts if you encounter rounding issues.')
    
    def compute_taxes(self): 

        for rec in self:

            if rec.amount_total:  
                rec.inverse_total_taxes =  rec.amount_total * (-1)
                
   
    def compute_untaxes(self): 

        for rec in self:
            if rec.amount_untaxed:  
                rec.inverse_total_untaxes =  rec.amount_untaxed * (-1) 
   
    @api.depends('line_ids.amount_currency', 'line_ids.tax_base_amount', 'line_ids.tax_line_id', 'partner_id', 'currency_id', 'amount_total', 'amount_untaxed')
    def _compute_inverse_tax_totals_json(self):
        """ Computed field used for custom widget's rendering.
            Only set on invoices.
        """
        for move in self:
            if not move.is_invoice(include_receipts=True):
                # Non-invoice moves don't support that field (because of multicurrency: all lines of the invoice share the same currency)
                move.inverse_tax_totals_json = None
                continue

            tax_lines_data = move._prepare_tax_lines_data_for_totals_from_invoice2() 

            move.inverse_tax_totals_json = json.dumps({
                **self._get_tax_totals(move.partner_id, tax_lines_data, move.inverse_total_taxes, move.inverse_total_untaxes, move.currency_id),
                'allow_tax_edition': move.is_purchase_document(include_receipts=False) and move.state == 'draft',
            })


    def _prepare_tax_lines_data_for_totals_from_invoice2(self, tax_line_id_filter=None, tax_ids_filter=None):
        """ Prepares data to be passed as tax_lines_data parameter of _get_tax_totals() from an invoice.

            NOTE: tax_line_id_filter and tax_ids_filter are used in l10n_latam to restrict the taxes with consider
                  in the totals.

            :param tax_line_id_filter: a function(aml, tax) returning true if tax should be considered on tax move line aml.
            :param tax_ids_filter: a function(aml, taxes) returning true if taxes should be considered on base move line aml.

            :return: A list of dict in the format described in _get_tax_totals's tax_lines_data's docstring.
        """
        self.ensure_one()

        tax_line_id_filter = tax_line_id_filter or (lambda aml, tax: True)
        tax_ids_filter = tax_ids_filter or (lambda aml, tax: True)

        balance_multiplicator = -1 if self.is_inbound() else 1
        tax_lines_data = []

        for line in self.line_ids:
            if line.tax_line_id and tax_line_id_filter(line, line.tax_line_id):
                tax_lines_data.append({
                    'line_key': 'tax_line_%s' % line.id,
                    'tax_amount': (line.amount_currency * balance_multiplicator) * (-1),
                    'tax': line.tax_line_id,
                })

            if line.tax_ids:
                for base_tax in line.tax_ids.flatten_taxes_hierarchy():
                    if tax_ids_filter(line, base_tax):
                        tax_lines_data.append({
                            'line_key': 'base_line_%s' % line.id,
                            'base_amount': line.amount_currency * balance_multiplicator,
                            'tax': base_tax ,
                            'tax_affecting_base': line.tax_line_id,
                        })

        return tax_lines_data   
                           