# -*- coding: utf-8 -*-
{
    'name': "Contact customizations",

    'summary': """
        Contact customizations module; Stores all new changes on the module.
        """,

    'description': """
        Contact customizations module; Stores all new changes on the module.
    """,

'author': "Abdessamad GERARD @ Captivea",
    'website': "https://www.captivea.us/",

    'category': 'Uncategorized',
    'version': '1.2',

    'depends': ['base', 'project','contacts','web_studio'],

    'data': [
        'security/ir.model.access.csv',
        'data/department_demo.xml',
        'data/automations.xml',
        'data/cron.xml',
        'data/server_actions.xml',
        'views/phone_numbers.xml',
        'views/contact_changes.xml',
        'views/maintenance_popup.xml',
        'views/contact_popup.xml',
        'views/contact_popup_form.xml',
        'views/internal_alert.xml',
        'views/contact_location_relationship_views.xml',
        'views/historical_views.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': True,
}
