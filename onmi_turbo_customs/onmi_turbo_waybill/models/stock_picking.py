from odoo import fields, models, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    total_net_weight = fields.Float("Total Net Weight", compute="_compute_total_net_weight")

    contractual_shipper = fields.Text("Contractual Shipper", default="RECICLADOS MEDIOAMBIENTALES TURBO PLASTIC SL\n"
                                                                     "ESB30768253\n"
                                                                     "Cr Cartagena-Alhama 25 30320 - Murcia España\n"
                                                                     "30333 Cuevas de Reyllo (Fuente Alamo)Murcia\n"
                                                                     "Tel.: 968151130.\n")
    comments = fields.Text("Comments")
    commodity = fields.Text("Nature of commodity", compute="_compute_commodity")

    signature_waybill = fields.Binary(string='Signature')

    net_weight = fields.Float("Net Weight", compute="_compute_net_weight")

    def _compute_net_weight(self):
        for rec in self:
            rec.net_weight = 0.0

            for w in rec.weighing_ids:
                rec.net_weight += w.final_weight + w.waste

    def _compute_total_net_weight(self):
        for rec in self:
            total = 0.0
            for line in rec.move_ids_without_package:
                total += line.quantity_done

            rec.total_net_weight = total

    def _compute_commodity(self):
        self.ensure_one()
        commodity = ""
        for op in self.move_ids_without_package:
            if op.product_id and op.product_id.default_code and op.product_id.name:
                commodity += "[" + op.product_id.default_code +"] " + op.product_id.name + "\n"
        if commodity != "":
            self.commodity = commodity[:-1]
        else:
            self.commodity = commodity

