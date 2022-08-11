# -*- coding: utf-8 -*-
{
    'name': "Accounting customizations",

    'summary': """
        Accounting customizations module; Stores all new changes on the module.
        """,

    'description': """
        Accounting customizations module; Stores all new changes on the module.
    """,

'author': "Abdessamad GERARD @ Captivea",
    'website': "https://www.captivea.us/",

    'category': 'Uncategorized',
    'version': '1.1',

    'depends': ['base','account'],

    'data': [
        'security/ir.model.access.csv',
        'views/register_payment.xml',
    ],
    'installable': True,
    'auto_install': True,
}
