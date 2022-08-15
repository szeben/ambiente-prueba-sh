# -*- coding: utf-8 -*-
{
    'name': "Referencia Bancaria Pagos",

    'summary': """
        Permitir especificar una Referencia Bancaria asociada a un pago, validando que no se emplee para varios 
        pagos.""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Techne Studio IT & Consulting",
    'website': "http://www.yourcompany.com",

    'category': 'account',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account'],

    # always loaded
    'data': [
        'views/account_payment_views.xml'
    ],
    # 'qweb': [
    #     'referencia_bancaria/static/src/xml/one_template.xml'
    # ],
    'assets': {
        'web.assets_backend': [
            'referencia_bancaria/static/src/js/javaScript.js',
            'referencia_bancaria/static/src/css/style.scss',

        ]
    }
}
