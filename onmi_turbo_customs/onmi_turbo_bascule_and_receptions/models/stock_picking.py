from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    license_plate_id = fields.Many2one('license.plate', tracking=True, )
    trailer_id = fields.Many2one('trailer', tracking=True, )

    upload_date = fields.Date(string="Fecha carga", tracking=True, )

    weighing_ids = fields.One2many('weighing', 'picking_id', string="Weighings")

    confirmed_weighings = fields.Boolean('Confirmed Weighing', default=False)

    active_reconfirm_new_weighings = fields.Boolean('Active new weighings', default=False)

    text_warning = fields.Text("Text Warning")

    weighings_is_required = fields.Boolean("Weighings is required")

    total_ordered = fields.Float(string="Total ordered", compute="_compute_totals")
    total_wasted = fields.Float(string="Total ordered", compute="_compute_totals")
    total_delivered = fields.Float(string="Total ordered", compute="_compute_totals")

    def _compute_totals(self):
        for rec in self:
            rec.total_ordered = 0.0
            rec.total_delivered = 0.0
            rec.total_wasted = 0.0
            for line in rec.move_ids_without_package:
                rec.total_ordered += line.product_uom_qty

                # En Odoo 18, parece que quantity_done ya no existe en stock.move
                # Obtenemos la cantidad hecha de las líneas de movimiento asociadas
                move_lines = self.env['stock.move.line'].search([
                    ('move_id', '=', line.id)
                ])
                qty_done = sum(move_line.qty_done for move_line in move_lines) if move_lines else 0.0
                rec.total_delivered += qty_done

            for w in rec.weighing_ids:
                rec.total_wasted += w.waste

    @api.onchange('license_plate_id')
    def asign_license_plate(self):
        """
        Si se rellena el campo de Matrícula del alabrán se asigna a todos los pesajes.
        :return:
        """
        for rec in self:
            if rec.license_plate_id:
                for weight in rec.weighing_ids:
                    weight.license_plate_id = rec.license_plate_id

    @api.onchange('trailer_id')
    def asign_trailer(self):
        """
        Si se rellena el campo de Remolque del alabrán se asigna a todos los pesajes.
        :return:
        """
        for rec in self:
            if rec.trailer_id:
                for weight in rec.weighing_ids:
                    weight.trailer_id = rec.trailer_id

    @api.onchange('upload_date')
    def asign_date(self):
        """
        Si se rellena el campo de FEcha de carga del alabrán se asigna a todos los pesajes.
        :return:
        """
        for rec in self:
            if rec.upload_date:
                for weight in rec.weighing_ids:
                    weight.upload_date = rec.upload_date

    def action_confirm_weighings(self):
        """
            Traspaso de Pesos finales a cantidades hechas de las operaciones y pasado a estado "Confirmado"
        si pasa las validaciones.

            * Validaciones:
                - Remloque o matricula no relleno (significa que Transporte no confirmado), Error.
                - Pesos finales > 0, en otro caso, Error.
                - Demanda de operaciones = Peso final, en otro caso, Error.

        :return:
        """
        if self.purchase_id and (not self.trailer_id or not self.license_plate_id):
            raise ValidationError(_("CARRIAGE ORDER NOT PROCESSED\n"
                                    "Carriage order related to this picking is not processed."
                                    " You will know that this is done if license plate and trailer take some value.\n"
                                    "Contact logistic workers to ask  for this."))
        not_final_weight = self.weighing_ids.filtered(lambda w: w.final_weight == 0)
        # Check if some weighing final weight isn´t calculated.
        if not_final_weight:
            raise ValidationError(_("Some Final Weight are <= 0.\n"
                                    "Maybe you forgot to put some weight on any lines of Weighing.\n"
                                    "Please, check if it is occurring."))
        # Check product uom qty with final weight
        for weight in self.weighing_ids:
            if weight.final_weight != weight.move_line_id.product_uom_qty:
                self.active_reconfirm_new_weighings = True
                self.text_warning = _("Some weighings are different from qty on picking.\n" \
                                      "If you want to take this weight you can press on the next button.\n")
                return True

        for weight in self.weighing_ids:
            # Obtenemos el move_line relacionado con este stock.move
            move_lines = self.env['stock.move.line'].search([
                ('move_id', '=', weight.move_line_id.id)
            ])

            if move_lines:
                for line in move_lines:
                    line.qty_done = weight.final_weight
            else:
                # Si no hay líneas, intentar crear una
                self.env['stock.move.line'].create({
                    'move_id': weight.move_line_id.id,
                    'product_id': weight.move_line_id.product_id.id,
                    'product_uom_id': weight.move_line_id.product_uom.id,
                    'location_id': weight.move_line_id.location_id.id,
                    'location_dest_id': weight.move_line_id.location_dest_id.id,
                    'qty_done': weight.final_weight,
                    'picking_id': self.id,
                })

            weight.state = 'confirmed'

        self.confirmed_weighings = True

    def action_reconfirm_weighings(self):
        for wg in self.weighing_ids:
            if wg.move_line_id:
                wg.move_line_id.product_uom_qty = wg.final_weight

                if wg.move_line_id.sale_line_id:
                    wg.move_line_id.sale_line_id.product_uom_qty = wg.final_weight

                if wg.move_line_id.purchase_line_id:
                    wg.move_line_id.purchase_line_id.product_qty = wg.final_weight

                move_lines = self.env['stock.move.line'].search([
                    ('move_id', '=', wg.move_line_id.id)
                ])

                if move_lines:
                    for line in move_lines:
                        line.qty_done = wg.final_weight
                else:
                    self.env['stock.move.line'].create({
                        'move_id': wg.move_line_id.id,
                        'product_id': wg.move_line_id.product_id.id,
                        'product_uom_id': wg.move_line_id.product_uom.id,
                        'location_id': wg.move_line_id.location_id.id,
                        'location_dest_id': wg.move_line_id.location_dest_id.id,
                        'qty_done': wg.final_weight,
                        'picking_id': self.id,
                    })

                wg.state = 'confirmed'

            self.confirmed_weighings = True
            self.active_reconfirm_new_weighings = False

    def action_reset_weighings(self):
        """
            Retorna a estado "En Pesaje", para volver a calcular los pesos finales.
        :return:
        """
        if self.state == 'done':
            raise ValidationError(_("PICKING DONE OR CANCEL\n"
                                    "You can't reset weighings if picking is on state Done or cancel.\n"
                                    "Please, check if it is occurring."))
        for wg in self.weighing_ids:
            wg.state = 'on_weighing'

        # Actualización para usar move_ids_without_package y acceder a qty_done en lugar de quantity_done
        for move in self.move_ids_without_package:
            # Reiniciar las cantidades en las líneas de movimiento
            move_lines = self.env['stock.move.line'].search([
                ('move_id', '=', move.id)
            ])
            for line in move_lines:
                line.qty_done = 0.0

            # Ya no usamos move.quantity_done = 0.0 porque no existe ese atributo en Odoo 18

        self.confirmed_weighings = False
        self.active_reconfirm_new_weighings = False

    def action_recalculate_weighings(self):
        for operation in self.move_ids_without_package:
            weighing_related = self.env['weighing'].search([
                ('picking_id', '=', self.id),
                ('move_line_id', '=', operation.id),
            ])
            if not weighing_related:
                if self.picking_type_id.sequence_code == 'IN':
                    type_assigned = 'input'
                else:
                    type_assigned = 'output'
                self.env['weighing'].create({
                    'product_id': operation.product_id.id,
                    'type': type_assigned,
                    'picking_id': self.id,
                    'move_line_id': operation.id,
                    'state': 'on_weighing',
                })

    def button_validate(self):
        """
            Herencia Validar albaranes.
            Antes de validar, revisa si los pesajes están confirmados,...
                - Si no lo están, Error.
                - Si sí lo están, Confirma las solicitudes de transporte relacionadas con el pedido del albarán.
        :return:
        """
        if not self.weighings_is_required:
            return super(StockPicking, self).button_validate()
        weighings_not_confirmed = self.weighing_ids.filtered(lambda w: w.state != 'confirmed')
        if weighings_not_confirmed:
            raise ValidationError(_("WEIGHINGS NOT CONFIRMED\n"
                                    "There are some weighing lines that are not confirmed.\n"
                                    "Please, check if it is occurring."))
        else:
            carriage_order_purchase = self.env['carriage.order'].search([('purchase_order_id.name', '=', self.origin)])
            carriage_order_sale = self.env['carriage.order'].search([('sale_order_id.name', '=', self.origin)])

            if carriage_order_purchase:
                carriage_order_purchase.state = 'confirm'
                carriage_order_purchase.processed = True
            if carriage_order_sale:
                carriage_order_sale.state = 'confirm'
                carriage_order_sale.processed = True
            return super(StockPicking, self).button_validate()
