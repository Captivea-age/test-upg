# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Cap_ custom CSS',
    'version' : '14.0.0.2',
    'summary': 'CSS',
    'description': """
Import Invoices
""",
    'category': 'Tools',
    'author': 'Captivea',
    'website': 'https://captivea.com',
    'depends' : [
        'base',
    ],
    'data': [
        'views/custom_scss.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
