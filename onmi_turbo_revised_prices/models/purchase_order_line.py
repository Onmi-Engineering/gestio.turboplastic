from odoo import fields, models, api
from odoo.exceptions import ValidationError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order.line'

    date_approve = fields.Datetime(related="order_id.date_approve")
    partner_id = fields.Many2one(related="order_id.partner_id")

    def action_confirm_revised(self):
        
        active_ids = self.env.context.get('active_ids', [])
        revised = self.env['purchase.order.line'].browse(active_ids) 
        for rec in self:
            
            lines_by_order = {}
            for line in revised:            
                if line.order_id.id not in lines_by_order:
                    lines_by_order[line.order_id.id] = [line]
                else:
                    lines_by_order[line.order_id.id].append(line)
            
            for order_id, lines in lines_by_order.items():
                order_lines = self.env['purchase.order.line'].search([('order_id', '=', order_id)])
                if len(lines) != len(order_lines):                
                    raise ValidationError('Debe seleccionar todas las líneas del pedido {} para marcar el check de precios revisados.'.format(lines[0].order_id.name))
                rec.order_id.check_revised = True
        
    

