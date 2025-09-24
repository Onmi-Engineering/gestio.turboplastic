from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    invoice_margin_ids = fields.Many2many('account.move.margin') 
    margin = fields.Float("Margin", compute="_compute_margin", store=True)
    rec_invoice = fields.Float("Rectificative invoice", compute="_compute_rectificative")
    percentaje = fields.Float("Percentaje", compute="_compute_percentaje", store=True)

    def _compute_rectificative(self):
      for rec in self: 
       if rec.reversal_move_ids:
        for li in  rec.reversal_move_ids:
         rec.rec_invoice = li.amount_total 
       else:
        rec.rec_invoice = False

    @api.depends("rec_invoice", "invoice_margin_ids.total", "invoice_margin_ids.invoice_id")
    def _compute_margin(self): 
      
      for rec in self:
        resul = rec.amount_total
        if  rec.reversal_move_ids:
            resul -= rec.amount_total
        for res in rec.invoice_margin_ids:                
          if rec.invoice_margin_ids:
                if res.invoice_id.move_type == 'in_invoice':           
                 resul -= res.total
                if res.invoice_id.move_type == 'in_refund':           
                 resul += res.total                                      
        rec.margin = resul if rec.invoice_margin_ids else False

    @api.depends("margin")        
    def _compute_percentaje(self):

      for rec in self:
        resul = rec.amount_total
        if  rec.reversal_move_ids:
         for dif in self.reversal_move_ids:
           resul -= dif.amount_total
        if  rec.margin > 0 and rec.amount_total > 0:    
          rec.percentaje =  rec.margin / rec.amount_total         
        else:
          rec.percentaje = 0.0

    def update_benefits(self): 

      self._compute_rectificative() 
      self._compute_margin()       
      self._compute_percentaje() 


    
        