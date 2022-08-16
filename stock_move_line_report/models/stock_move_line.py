# -*3- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, api, fields, _
import re

class StockMoveLine(models.Model):
    #_name = "account.aged.partner.inherit"
    _inherit = 'stock.move.line'


    codigo_id = fields.Many2one('res.users', string='Codigo',)
    number = fields.Char(string='Numero',related='picking_id.origin')
    customer_id = fields.Many2one('res.partner', string='Cliente o Proveedor',related='picking_id.partner_id')
    entrada = fields.Float(string='Entrada',compute='_compute_entrada')
    salida = fields.Float(string='Salida',compute='_compute_salida')
    saldo_existencia = fields.Float(string='Saldo en existencia', compute='_compute_saldo_existencia')

    @api.depends('qty_done','reference')
    def _compute_entrada(self):        
        for record in self:
            #   Cantidad de producto actualizada
            if record.location_id.id == 14 and record.location_id.name == 'Inventory adjustment':
                record.entrada = record.qty_done

            # Recibo
            elif record.picking_code == "incoming":
                record.entrada = record.qty_done

            #Transferencia Interna
            elif record.picking_code == "internal":
                record.entrada = record.qty_done

            #Fabricacion
            elif record.picking_code == "mrp_operation":
                record.entrada = record.qty_done
            else:
                record.entrada = 0.0

    @api.depends('qty_done','reference')
    def _compute_salida(self):
        for record in self:
            #   Cantidad de producto actualizada
            if record.location_id.id == 14 and record.location_dest_id.name == 'Inventory adjustment':
                record.salida = record.qty_done

            #Transferencia Interna
            elif record.picking_code == "internal":
                record.salida = record.qty_done

            #Envio
            elif record.picking_code == "outgoing":
                record.salida = record.qty_done

            else:
                record.salida = record.qty_done

    @api.depends('entrada','salida')
    def _compute_saldo_existencia(self):
        for record in self:
            #record.saldo_existencia = record.salida + record.entrada
            record.saldo_existencia = 0.0