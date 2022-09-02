# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _, api
import datetime
import pdb


class StockInventoryReposition(models.TransientModel):
    _name = 'stock.inventory.reposition'
    _description = 'Inventory Reposition'

    # def default_get(self, fields_list):
    #     res = super().default_get(fields_list)
    #     if self.env.context.get('default_quant_ids'):
    #         quants = self.env['stock.quant'].browse(self.env.context['default_quant_ids'])
    #         res['show_info'] = any(not quant.inventory_quantity_set for quant in quants)
    #     return res

    #def _default_inventory_adjustment_name(self):
        #return _("Reposicion de Inventaro") + " - " + fields.Date.to_string(fields.Date.today())

    #quant_ids = fields.Many2many('stock.quant')
    #inventory_adjustment_name = fields.Char(default=_default_inventory_adjustment_name)
    show_info = fields.Boolean('Show warning')
    desde_fecha = fields.Date(string='Desde', default=lambda self: fields.Date.today())
    hasta_fecha = fields.Date(string='Hasta', compute='_compute_hasta_fecha')

    _depends = {
        'account.move': [
            'name', 'state', 'move_type', 'partner_id', 'invoice_user_id', 'fiscal_position_id',
            'invoice_date', 'invoice_date_due', 'invoice_payment_term_id', 'partner_bank_id',
        ],
        'account.move.line': [
            'quantity', 'price_subtotal', 'amount_residual', 'balance', 'amount_currency',
            'move_id', 'product_id', 'product_uom_id', 'account_id', 'analytic_account_id',
            'journal_id', 'company_id', 'currency_id', 'partner_id',
        ],
        'product.product': ['product_tmpl_id'],
        'product.template': ['categ_id'],
        'uom.uom': ['category_id', 'factor', 'name', 'uom_type'],
        'res.currency.rate': ['currency_id', 'name'],
        'res.partner': ['country_id'],
    }

    @api.depends('desde_fecha')
    def _compute_hasta_fecha(self):
        self.hasta_fecha = self.desde_fecha + datetime.timedelta(days=15)

    # @property
    # def _table_query(self):
    #     return '%s %s %s' % (self._select(), self._from(), self._where())

    # @api.model
    # def _select(self):
    #     return '''
    #         SELECT

    #         '''

    # @api.model
    # def _from(self):
    #     return '''
    #         FROM stock.quant
    #     '''

    # @api.model
    # def _where(self):
    #     return '''
    #         WHERE move.move_type IN ('out_invoice', 'out_refund', 'in_invoice', 'in_refund', 'out_receipt', 'in_receipt')
    #             AND line.account_id IS NOT NULL
    #             AND NOT line.exclude_from_invoice_tab
    #     '''

    
    def action_apply(self):

        # Crear Logica para obtener la consulta de reposicion de inventario desde la fecha seleccionada hasta 15 dias despues de la seleccionada
        compania = self.env.user.company_id
        quants = self.env['stock.quant'].search([('company_id','=',compania.id)])
        reposiciones = self.env['stock.quant.reposition'].search([])
        products = self.env['product.product'].search([('type','=','product')])
            
        if quants and reposiciones and products:
            reposiciones = self.env['stock.quant.reposition']
            for quant in quants:
                if quant.location_id.location_id.name == 'WHCCS':
                    quant_ccs = quant.quantity
                producto = quant.product_id.id
                name_categoria = quant.product_id.categ_id.name + ' ' + quant.product_id.name
                for repo in reposiciones:
                    if repo.product_id.id == quant.product_id.id:
                        update = reposiciones.write({'product_id' : producto, 'producto': name_categoria, 'deposito_principal_ccs': quant_ccs})
        elif quants and products:
            #Recorro los productos
            reposiciones = self.env['stock.quant.reposition']
            quant_ccs = 0.0
            quant_mgt = 0.0
            quant_bto = 0.0
            quant_val = 0.0
            for product in products:
                product_id = product.id
                quant_product = self.env['stock.quant'].search([('product_id','=',product_id)])
                #recorro los quants de cada producto
                name_categoria = product.categ_id.name + ' ' + product.name
                

                for qproduct in quant_product:
                    # is_main = qproduct.location_id.is_main
                    # if is_main == True:
                    #Rama Caracas WHCCS
                    if qproduct.location_id.warehouse_id.branch_id.id == 1:
                        quant_ccs = qproduct.quantity
                        #new = reposiciones.create({'product_id' : producto, 'producto': name_categoria, 'deposito_principal_ccs': quant_ccs})
                    #Rama Barquisimeto WHBTO
                    if qproduct.location_id.warehouse_id.branch_id.id == 2:
                        quant_bto = qproduct.quantity
                        #new = reposiciones.create({'product_id' : producto, 'producto': name_categoria, 'deposito_principal_bto': quant_bto})
                    #Rama Margarita WHMgt
                    if qproduct.location_id.warehouse_id.branch_id.id == 3:
                        quant_mgt = qproduct.quantity
                        #new = reposiciones.create({'product_id' : producto, 'producto': name_categoria, 'deposito_principal_mgta': quant_mgt})
                    #Rama Valencia WHVAL
                    if qproduct.location_id.warehouse_id.branch_id.id == 4:
                        quant_val = qproduct.quantity
                        #new = reposiciones.create({'product_id' : producto, 'producto': name_categoria, 'deposito_principal_val': quant_val})
                new = reposiciones.create({'product_id' : product_id, 'producto': name_categoria, 'deposito_principal_mgta': quant_mgt, 'deposito_principal_ccs': quant_ccs, 'deposito_principal_bto': quant_bto, 'deposito_principal_val': quant_val})


        return {
                'type': 'ir.actions.client',
                'tag': 'reload',
                }





        #self.env.cr.execute("""CREATE or REPLACE VIEW %s as (
        # quant = self.env.cr.execute("""
        #                    SELECT
        #                       %s
        #                    FROM
        #                       %s
        #                     WHERE
        #                       %S
        #   """ % (self._table_query, self._select(), self._from(),self._where()))
        #return 0
        ########################
        


        #return self.quant_ids.with_context(
        #    inventory_name=self.inventory_adjustment_name).action_apply_inventory()
    
    