# -*- coding: utf-8 -*-
{
    'name': "Project customizations",

    'summary': """
        Project customizations module; Stores all new changes on the module.
        """,

    'description': """
        Project customizations module; Stores all new changes on the module.
    """,

    'author': "Abdessamad GERARD @ Captivea",
    'website': "https://www.captivea.us/",

    'category': 'Uncategorized',
    'version': '1.1',

    'depends': ['base', 'project','web_studio','contacts','industry_fsm'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/task_custom.xml'

    ],
    'installable': True,
    'auto_install': True,
}
