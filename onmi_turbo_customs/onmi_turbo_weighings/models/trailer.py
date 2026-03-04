from odoo import fields, models


class Trailer(models.Model):
    _name = 'trailer'
    _description = 'Trailer'

    name = fields.Char(string="Identificator")
    description = fields.Char(string="Description")
    license_plate_id = fields.Many2one('license.plate', required=False)
    weighing_count = fields.Integer('Weighing Count', compute='_compute_weighing_ids')
    weighing_ids = fields.Many2many('weighing', string="Weighings", compute='_compute_weighing_ids')

    _sql_constraints = [
        ('name_uniq_trailer', 'unique (name)', 'You can not have two trailers with the same name!')
    ]

    def _compute_weighing_ids(self):
        for rec in self:
            rec.weighing_ids = self.env['weighing'].search([('trailer_id', '=', rec.id)])
            rec.weighing_count = len(rec.weighing_ids)

    def _get_action_view_weighings(self, weighings):
        """
        This function returns an action that display existing carriages orders
        of given sales order ids. It can either be in a list or in a form
        view, if there is only one carriage order to show.
        """

        action = self.env["ir.actions.actions"]._for_xml_id(
            "onmi_turbo_weighings.onmi_action_weighing")

        if len(weighings) > 1:
            action['domain'] = [('id', 'in', weighings.ids)]
            action['view_id'] = (
                self.env.ref('onmi_turbo_weighings.weighing_tree_view').id,
                'carriage_order.tree.view.action'
            )
            action['views'] = []
            action['view_mode'] = 'tree'
        elif weighings:
            form_view = [
                (self.env.ref('onmi_turbo_weighings.weighing_form_view').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = weighings.id
        # Prepare the context.
        action['context'] = dict(self._context, default_trailer_id=self.id)
        return action

    def action_view_weighings(self):
        return self._get_action_view_weighings(self.weighing_ids)
