# -*- coding: utf-8 -*-
{
    'name': "Referencia Bancaria Pagos",
    'summary': "Permitir especificar una Referencia Bancaria asociada a un pago, validando que no se emplee para varios pagos.",
    "description": """
        Incluye número de referencia único para los pagos realizados por vías bancarias (transferencias, zelle, etc).
    """,
    'author': "Techne Studio IT & Consulting",
    'website': "http://www.yourcompany.com",
    'category': 'account',
    'version': '0.1',
    'depends': ['account','sale_management'],
    'data': [
        'views/account_payment_register_views.xml',
        'views/account_payment_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'referencia_bancaria/static/src/js/javaScript.js',
            'referencia_bancaria/static/src/css/style.scss',
        ]
    }
}
