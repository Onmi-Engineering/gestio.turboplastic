import logging
from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

class CarriageOrder(models.Model):
    _name = 'carriage.order'
    _description = 'Carriage Orders'

    name = fields.Char(string="name", default=_('New'))
    contact = fields.Many2one('res.partner')
    partner_shipping_alt = fields.Char('Alternative Delivery Address')
    weight = fields.Float('Approximate weight')
    weight_uom = fields.Many2one('uom.uom', string='Unit of Measure', compute="_compute_weight_uom", store=False)
    processed = fields.Boolean('Not Processed/ Processed', compute='_compute_processed', store=True)
    origin = fields.Char('Origin', compute='compute_origin', store=True)
    sale_order_id = fields.Many2one('sale.order', 'Sale Order #', readonly=True)
    purchase_order_id = fields.Many2one('purchase.order', 'Purchase Order #', readonly=True)
    license_plate_id = fields.Many2one('license.plate')
    trailer_id = fields.Many2one('trailer')
    pick_up_date = fields.Datetime('Pick Up Date')
    delivery_date = fields.Datetime('Delivery Date')
    state = fields.Selection(string='Status', required=True, readonly=True, copy=False, selection=[
        ('draft', 'New'),
        ('processing', 'Processing'),
        ('processed', 'Processed'),
        ('confirm', 'Delivered'),
        ('cancel', 'Cancelled'),
    ], default='draft',
                             help="The current state of your carriage order:"
                                  "- New: Fully editable"
                                  "- Processing: No longer editable"
                                  "- Processed: Processed"
                                  "- Validated: Finished"
                                  "- Cancelled: Cancelled"
                             )
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    def _compute_weight_uom(self):
        for rec in self:
            rec.weight_uom = self.env['uom.uom'].search([('name', '=', 'kg')], limit=1)


    @api.depends('sale_order_id', 'purchase_order_id')
    def compute_origin(self):
        for rec in self:
            rec.origin = ''
            if rec.sale_order_id:
                rec.origin = rec.sale_order_id.name
            if rec.purchase_order_id:
                rec.origin = rec.purchase_order_id.name

    @api.onchange('state')
    def _compute_processed(self):
        for rec in self:
            if rec.state == 'processed':
                rec.processed = True
            else:
                rec.processed = False

    def action_processed(self):
        for rec in self:
            if not rec.trailer_id or not rec.license_plate_id:
                raise ValidationError(_("MISSING DATA TO FILL\n"
                                        "You have to fill data of license plate and trailer to processed.\n"
                                        "Please, check if it is occurring."))
            else:
                if rec.sale_order_id:
                    pickings_sale = self.env['stock.picking'].search([('sale_id', '=', rec.sale_order_id.id)])
                    if pickings_sale:
                        for sps in pickings_sale:
                            sps.trailer_id = rec.trailer_id
                            sps.license_plate_id = rec.license_plate_id
                            if sps.weighing_ids:
                                for weigh in sps.weighing_ids:
                                    weigh.trailer_id = sps.trailer_id
                                    weigh.license_plate_id = sps.license_plate_id
                if rec.purchase_order_id:
                    pickings_purchase = self.env['stock.picking'].search([('purchase_id', '=', rec.purchase_order_id.id)])
                    if pickings_purchase:
                        for spp in pickings_purchase:
                            spp.trailer_id = rec.trailer_id
                            spp.license_plate_id = rec.license_plate_id
                            if spp.weighing_ids:
                                for weigh in spp.weighing_ids:
                                    weigh.trailer_id = spp.trailer_id
                                    weigh.license_plate_id = spp.license_plate_id
                rec.write({'state': 'processed'})
                rec.write({'processed': True})

    def action_cancelled(self):
        for rec in self:
            rec.write({'state': 'cancel'})
            rec.write({'processed': False})

    def action_processing(self):
        for rec in self:
            rec.write({'state': 'processing'})
            rec.write({'processed': False})

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name') == _('New') or vals.get('name') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('carriage.order')
            vals['state'] = 'processing'
        return super().create(vals_list)

    def unlink(self):
        for rec in self:
            if rec.name != _('New'):
                seq = self.env['ir.sequence'].search([('code', '=', 'carriage.order')], limit=1)
                seq.number_next_actual -= 1
        return super().unlink()
