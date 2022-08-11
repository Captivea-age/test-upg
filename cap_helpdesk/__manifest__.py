# -*- coding: utf-8 -*-
{
    'name': "Helpdesk customizations",

    'summary': """
        Helpdesk customizations module; Stores all new changes on the module.
        """,

    'description': """
        Helpdesk customizations module; Stores all new changes on the module.
    """,

    'author': "Abdessamad GERARD @ Captivea",
    'website': "https://www.captivea.us/",

    'category': 'Uncategorized',
    'version': '1.1',

    'depends': ['base', 'helpdesk','project','industry_fsm','web_studio','helpdesk_fsm','preventive_maintenance'],

    'data': [
        'security/ir.model.access.csv',
        'data/automations.xml',
        'data/cron.xml',
        'views/helpdesk_custom.xml',
        'views/contact_form.xml',
    ],
    'installable': True,
    'auto_install': True,
}
