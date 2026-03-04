from odoo import fields, models, api,_
from odoo.exceptions import ValidationError


class Weighing(models.Model):
    _name = 'weighing'
    _description = 'Weighing records'

    type = fields.Selection([
        ('input', 'Input'),
        ('output', 'Output')
    ])
    state = fields.Selection([
        ('new', 'New'),
        ('on_weighing', 'On weighing'),
        ('confirmed', 'Confirmed'),
    ])
    first_weight = fields.Float('First Weight')
    second_weight = fields.Float('Second Weight')
    waste = fields.Float('Waste')
    final_weight = fields.Float('Final Weight', compute='compute_final_weight', default=0.0, store=True)
    product_id = fields.Many2one('product.product', 'Product', check_company=True, domain="[('type', 'in', ['product', 'consu'])]", required=True)
    license_plate_id = fields.Many2one('license.plate')
    trailer_id = fields.Many2one('trailer')
    upload_date = fields.Date(string="Fecha carga", store=True)
    contact = fields.Many2one('res.partner')
    picking_id = fields.Many2one('stock.picking')
    sale_id = fields.Many2one('sale.order')
    purchase_id = fields.Many2one('purchase.order')
    move_line_id = fields.Many2one('stock.move')
    code_led = fields.Char(string="L.E.R")
    description = fields.Text('Description', compute='compute_final_descripcion')
    partner_picking = fields.Char('res.partner', compute='compute_partner_picking', store=True)
    date_done_picking = fields.Datetime(string="Entry date", compute="_compute_date_done_picking", store=True)
    final_weight_calculate = fields.Float('Final Weight', compute='compute_final_weight_calculate', store=True)
    company_id = fields.Many2one('res.company', compute='_compute_company_id', store=True)
    picking_state = fields.Selection(related='picking_id.state', store=True)

    @api.depends('first_weight', 'second_weight', 'waste')
    def compute_final_weight(self):
        for rec in self:
            rec.final_weight = 0.0
            if rec.first_weight and rec.second_weight:
                if rec.first_weight > 0.0 and rec.second_weight > 0.0:
                    # Come from SALE ORDERS
                    if rec.type == 'output':
                        if rec.first_weight > rec.second_weight:
                            raise ValidationError(
                                _('First Weight can´t be upper than second one on Weighings from Sale Orders.\n'
                                  'Please, check this value for the correct calculation.\n'))
                        rec.final_weight = rec.second_weight - rec.first_weight - rec.waste

                    # Come from PURCHASE ORDERS
                    if rec.type == 'input':
                        if rec.first_weight < rec.second_weight:
                            raise ValidationError(
                                _('Second Weight can´t be upper than first one on Weighings from Purchase Orders.\n'
                                  'Please, check these values for the correct calculation.\n'))
                        rec.final_weight = rec.first_weight - rec.second_weight - rec.waste

    @api.onchange('waste')
    def update_final_weight(self):
        for rec in self:
            if rec.waste > 0.0:
                if rec.type == 'output':
                    rec.final_weight = rec.second_weight - rec.first_weight - rec.waste
                if rec.type == 'input':
                    rec.final_weight = rec.first_weight - rec.second_weight - rec.waste

    def _compute_date_done_picking(self):
        for rec in self:
            if rec.picking_id:
                rec.date_done_picking = rec.picking_id.scheduled_date

    def _compute_company_id(self):
        for rec in self:
            if rec.picking_id:
                rec.company_id = rec.picking_id.company_id
            else:
                rec.company_id = False

    def compute_partner_picking(self):
        for rec in self:
            if rec.picking_id:
                rec.partner_picking = rec.picking_id.partner_id.name
            else:
                rec.partner_picking = _('not defined')

    @api.depends('first_weight', 'second_weight')
    def compute_final_weight_calculate(self):
        for rec in self:
            rec.final_weight_calculate = 0.0
            if rec.first_weight and rec.second_weight:
                if rec.first_weight > 0.0 and rec.second_weight > 0.0:
                    # Come from SALE ORDERS
                    if rec.type == 'output':
                        if rec.first_weight > rec.second_weight:
                            raise ValidationError(
                                _('First Weight can´t be upper than second one on Weighings from Sale Orders.\n'
                                  'Please, check this value for the correct calculation.\n'))
                        rec.final_weight_calculate = rec.second_weight - rec.first_weight - rec.waste

                    # Come from PURCHASE ORDERS
                    if rec.type == 'input':
                        if rec.first_weight < rec.second_weight:
                            raise ValidationError(
                                _('Second Weight can´t be upper than first one on Weighings from Purchase Orders.\n'
                                  'Please, check these values for the correct calculation.\n'))
                        rec.final_weight_calculate = rec.first_weight - rec.second_weight - rec.waste

    def compute_final_descripcion(self):
        for rec in self:
            sale = rec.move_line_id.sale_line_id    
            purchase =  rec.move_line_id.purchase_line_id
            rec.description = False                                 
            if  rec.sale_id.order_line:
              for line in rec.sale_id.order_line:                   
                    if line.product_id:                        
                            if line ==  sale:                                                             
                                if line.name != line.product_id.name and line.name != line.product_id.display_name:
                                 rec.description = line.name
            if  rec.purchase_id.order_line:
             for li in rec.purchase_id.order_line:                   
                    if li.product_id:              
                            if li ==  purchase:                             
                                if li.name != li.product_id.name and li.name != li.product_id.display_name:
                                 rec.description = li.name