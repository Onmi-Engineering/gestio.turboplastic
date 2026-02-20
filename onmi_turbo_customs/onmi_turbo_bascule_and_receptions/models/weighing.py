from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


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

    product_id = fields.Many2one(
        'product.product', 'Product', check_company=True,
        domain="[('type', 'in', ['product', 'consu'])]",
        required=True)

    license_plate_id = fields.Many2one('license.plate')
    trailer_id = fields.Many2one('trailer')

    upload_date = fields.Date(string="Fecha carga", store=True)


    contact = fields.Many2one('res.partner')
    picking_id = fields.Many2one('stock.picking')
    sale_id = fields.Many2one('sale.order')
    purchase_id = fields.Many2one('purchase.order')
    move_line_id = fields.Many2one('stock.move')

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

    # def set_final_weight(self):

    #     print('HOLA!!!!!!!!!!!!!!')
    #     self.compute_final_weight()