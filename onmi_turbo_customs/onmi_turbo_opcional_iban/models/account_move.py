from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    first_iban = fields.Char(default="ES35 3058 0236 0127 2021 6393(CAJAMAR)")
    second_iban = fields.Char(default="ES15 0182 6729 0402 0156 5081(BBVA)")
    third_iban = fields.Char(default="ES55 0081 1062 1100 0114 1618(SABADELL)")
    four_iban = fields.Char(default="ES43 3058 0236 0127 9900 0037 (CAJAMAR)")
    santander_iban = fields.Char(default="ES54 0049 2883 5127 1405 2631(SANTANDER)")
    cajamar_export_text = fields.Text(
        default="BANK NAME: CAJAMAR CAJA RURAL\n"
                "ADRESS: AV.MIGUEL DE CERVANTES 9,30009 MURCIA(ESPAÑA)\n"
                "EURO ACCOUNT: ES35 3058 0236 0127 2021 6393\n"
                "BIC:CCRIES2AXXX")
    santander_export_text = fields.Text(
        default="BANK NAME: BANCO SANTANDER S. A.\n"
                "ADRESS: C/SANTO DOMINGO, 10, 16440 MONTALBO, CUENCA(ESPAÑA)\n"
                "EURO ACCOUNT: ES54 0049 2883 5127 1405 2631\n"
                "BIC:BSCHESMM")
    show_first = fields.Boolean('CAJAMAR')
    show_second = fields.Boolean('BBVA')
    show_third = fields.Boolean('SABADELL')
    show_four = fields.Boolean('CAJAMAR (USD)')
    show_santander = fields.Boolean('SANTANDER')
    show_export_cajamar = fields.Boolean('CAJAMAR')
    show_export_santander = fields.Boolean('SANTANDER')
    id_company = fields.Integer("ID", compute="_compute_prueba")


    def _compute_prueba(self):
        self.id_company = self.company_id.id

