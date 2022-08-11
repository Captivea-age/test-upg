# -*- coding: utf-8 -*-
{
    'name': "Field service customizations",

    'summary': """
        Field service customizations module; Stores all new changes on the module.
        """,

    'description': """
        Field service customizations module; Stores all new changes on the module.
    """,

    'author': "Abdessamad GERARD @ Captivea",
    'website': "https://www.captivea.us/",

    'category': 'Uncategorized',
    'version': '1.1',

    'depends': ['base', 'project','web_studio','contacts','industry_fsm', 'industry_fsm_sale'],

    'data': [
        'security/ir.model.access.csv',
        'data/team_color_demo.xml',
        'data/automations.xml',
        'data/cron.xml',
        'data/server_actions.xml',
        'views/arrival_window.xml',
        'views/technician_view.xml',
        'views/time_selection_view.xml',
        'views/team_color_view.xml',
        'views/zip_list_view.xml',
        'views/actions.xml',
        'views/menu_items.xml',
        'views/followup_department.xml',
        'views/field_service_custom.xml',
        'views/res_partner_views.xml',
        'views/product_product_views.xml',
        'views/material_popup.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': True,
}
