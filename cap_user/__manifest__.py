# -*- coding: utf-8 -*-
{
    'name': "User customizations",

    'summary': """
        User customizations module; Stores all new changes on the module.
        """,

    'description': """
        User customizations module; Stores all new changes on the module.
    """,

'author': "Thomas PETITHORY @ Captivea",
    'website': "https://www.captivea.com/",

    'category': 'Uncategorized',
    'version': '1.1',

    'depends': ['base', 'cap_field_service'],

    'data': [
        'views/res_users_views.xml',
        'views/project_task_views.xml',
    ],
    'installable': True,
    'auto_install': True,
}
