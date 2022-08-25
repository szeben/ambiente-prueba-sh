# -*- coding: utf-8 -*-
{
    'name': 'Informe reposición de inventario',

    'summary': """
            Informe reposición de inventario
        """,

    'description': """
        Nueva vista de en los informes en el módulo de inventario, llamado Reposición de Inventario.
    """,

    'author': "Techne Studio IT & Consulting",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/stock_quant_reposition_tree.xml',
        'wizard/stock_inventory_reposition.xml',
    ],
    # only loaded in demonstration mode
    #'demo': [
    #    'demo/demo.xml',
    #],
}
