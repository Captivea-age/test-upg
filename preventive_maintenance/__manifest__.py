# -*- coding: utf-8 -*-
{
    'name': "Preventive Maintenance",

    'summary': """
        Preventive Maintenance module
        """,

    'description': """

    """,

    'author': "Abdessamad GERARD @ Captivea",
    'website': "https://www.captivea.us/",

    'category': 'Uncategorized',
    'version': '2.1',

    'depends': ['base', 'mail','helpdesk','project','sale_subscription'],

    'data': [
        'security/ir.model.access.csv',
        'data/pm_automations.xml',
        'data/pm_cron.xml',
        'views/airflow_component.xml',
        'views/component_views.xml',
        'views/equipment_views.xml',
        'views/maintenance_views.xml',
        'views/section_views.xml',
        'views/skill_views.xml',
        'views/system_location_views.xml',
        'views/system_type_views.xml',
        'views/system_views.xml',
        'views/test_category_views.xml',
        'views/test_records_views.xml',
        'views/test_views.xml',
        'views/test_list_views.xml',
        'views/notification_dashboard.xml',
        'views/notification.xml',
        'views/menu_items.xml',
        'wizard/add_return.xml',
        'wizard/add_supply.xml',
        'views/brand_views.xml',
        'views/project_task.xml',
    ],
    'installable': True,
    'auto_install': False,
}
