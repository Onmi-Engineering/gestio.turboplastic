from odoo import fields, models, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    check_revised = fields.Boolean(default=False)


    def update_purchase(self):
        for rec in self:
             if rec.invoice_status == 'invoiced':
                 rec.check_revised = True

    def update_check_false(self):
           active_ids = self.env.context.get('active_ids', [])
           revised = self.env['purchase.order'].browse(active_ids) 
           for rec in revised:
                rec.check_revised = False           

                self.picking_ids.move_line_ids.move_id.weighing_id.first_weight

                self.picking_ids.purchase_id.order_line.product_qty
                self.picking_ids.weighing_ids.purchase_id.order_line.product_qty