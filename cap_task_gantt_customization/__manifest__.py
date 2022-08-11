# -*- coding: utf-8 -*-
{
    'name': "Task Gantt Customization",
    'summary': """Display tag image on gatt view of the Project/FieldService Task.""",
    'description': """
    
Odoo Web Gantt chart view Tag Image.
======================================
1) Set Image on tag.
2) Set tag on project task Or filed service task.
3) Display that image on gatt view of the task.  

    """,
    'author': 'Konsultoo Software Consulting PVT. LTD.',
    'maintainer': 'Konsultoo Software Consulting PVT. LTD.',
    'contributors': ["Konsultoo Software Consulting PVT. LTD."],
    'website': 'https://www.konsultoo.com/',
    'category': 'Hidden',
    'version': '14.0.0.2.0',
    'depends': ['web_gantt', 'project_enterprise', 'cap_field_service', 'cap_studio_customization','industry_fsm'],
    'data': [
        'views/project_tags_views.xml',
        'views/project_task_views.xml',
        'views/task_gantt_view.xml',
        'views/templates.xml',
    ],
    'images': ['static/description/img/banner.gif', 'static/description/img/icon.png'],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'license': 'OPL-1',
    'installable': True,
    'application': False,
    'auto_install': False
}
