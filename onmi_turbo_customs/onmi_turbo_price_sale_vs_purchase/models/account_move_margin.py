from odoo import fields, models, api, _


class AccountMoveMargin(models.Model):
    _name = 'account.move.margin'

    invoice_id = fields.Many2one('account.move')
    name = fields.Char(related="invoice_id.name")
    total = fields.Float(compute="_compute_total")

    def _compute_total(self):

        busq = self.env['account.move'].search(['|',
            ('move_type', '=', 'in_refund') , ('move_type', '=', 'in_invoice')])
        for rec in self:
         for bus in busq:
                
            if self.invoice_id:
                if rec.invoice_id.id == bus.id:
                  
                         rec.total = rec.invoice_id.amount_total
            else:
                        rec.total = False

                     