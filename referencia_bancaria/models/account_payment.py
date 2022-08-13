# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class accountPaymeRegister(models.TransientModel):
    _inherit = "account.payment.register"

    referencia = fields.Char(string="Nro. Referencia", copy=False, help="Ingrese el Nro. de Referencia del Banco")

    _sql_constraints = [
        ('referencia_unique', 'unique(referencia)', 'Nro. de Referencia ya existe!')
    ]

    def action_create_payments(self):

        if self.referencia == False and self.journal_id.id == 7:
            raise ValidationError('El Campo Nro. de Referencia no puede estar Vacio')
        else:
            self._create_payments()
