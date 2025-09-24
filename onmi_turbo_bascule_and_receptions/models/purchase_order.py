from odoo import fields, models, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    carriage_ids = fields.Many2many('carriage.order', compute='_compute_carriage_ids',
                                    string='Carriages associated to this manufacturing order')
    carriage_count = fields.Integer(string='Carriage Orders', compute='_compute_carriage_ids')

    def _compute_carriage_ids(self):
        for rec in self:
            rec.carriage_ids = self.env['carriage.order'].search([('purchase_order_id', '=', rec.id)])
            rec.carriage_count = len(rec.carriage_ids)
    def button_confirm(self):
        """
        Herencia confirmar PO.

        Se crean tantos pesajes como operaciones tengan los albaranes creados.
        :return:
        """
        super(PurchaseOrder, self).button_confirm()

        if self.picking_ids:
            for picking in self.picking_ids:

                picking.weighings_is_required = True
                for operation in picking.move_ids_without_package:
                    self.env['weighing'].create({
                        'contact': self.partner_id.id,
                        'product_id': operation.product_id.id,
                        'type': 'input',
                        'picking_id': picking.id,
                        'purchase_id': self.id,
                        'move_line_id': operation.id,
                        'state': 'on_weighing',

                    })

    def action_create_carriage_order(self):
        """
        Crea Solicitud de Transporte con peso = suma de todas las cantidades.
        :return:
        """
        weight = 0
        for line in self.order_line:
            if line.product_qty:
                weight += line.product_qty

        ctx = {
            "default_purchase_order_id": self.id,
            "default_contact": self.partner_id.id,
            "default_weight": weight,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'carriage.order',
            'views': [
                (self.env.ref('onmi_turbo_bascule_and_receptions.carriage_order_form_view_for_action').id, 'form')],
            'view_id': self.env.ref('onmi_turbo_bascule_and_receptions.carriage_order_form_view_for_action').id,
            'target': 'new',
            'context': ctx,
        }

    def _get_action_view_carriage(self, carriages):
        '''
        This function returns an action that display existing carriages orders
        of given sales order ids. It can either be in a list or in a form
        view, if there is only one carriage order to show.
        '''
        action = self.env["ir.actions.actions"]._for_xml_id(
            "onmi_turbo_bascule_and_receptions.onmi_action_carriage_order")

        if len(carriages) > 1:
            action['domain'] = [('id', 'in', carriages.ids)]
            action['view_id'] = (
                self.env.ref('onmi_turbo_bascule_and_receptions.carriage_order_tree_view_for_action').id,
                'carriage_order.tree.view.action'
            )
            action['views'] = []
            action['view_mode'] = 'tree'
        elif carriages:
            form_view = [
                (self.env.ref('onmi_turbo_bascule_and_receptions.carriage_order_form_view_for_action').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = carriages.id
        # Prepare the context.
        action['context'] = dict(self._context, default_partner_id=self.partner_id.id,
                                 default_sale_order_id=self.id, default_origin=self.name)
        return action

    def action_view_carriage(self):
        return self._get_action_view_carriage(self.carriage_ids)
