from odoo import fields, models, api
import datetime
import re

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    num_identidication = fields.Char('Número de Identificación', compute="_compute_num_identidication",
                                     help="(XXXXXXXXXX) + (AAAA) + (YYYYYYY) Siendo X: NIMA del centro que genera la documentación.   Siendo A: Año en que se realiza el traslado. Siendo Y: Contador de 7 dígitos. Diferente para cada traslado")
    carrier_partner_id = fields.Many2one('res.partner', string='Transportista', domain="[('check_carrier', '=', True)]")
    
    
    @api.depends('name')
    def _compute_num_identidication(self):

        nima = 00000
        year = 2023
        numero_con_ceros = 1234567
        for rec in self:
            nombre = rec.name
            match = re.search(r'\d+$', nombre)
            if match:
                numero_extraido = match.group()                
                numero_con_ceros = numero_extraido.zfill(7)
            nima =rec.company_id.partner_id.nima
            year = datetime.datetime.now().year
            self.num_identidication = f'{nima}{year}{numero_con_ceros}'
             
   