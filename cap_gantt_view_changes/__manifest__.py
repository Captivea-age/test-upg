# -*- coding: utf-8 -*-

{
    "name": "Cap Gantt View Changes",
    "version": "1.0",
    'author': "Captivea",
    'website': "www.captivea.us",
    "category": "Web",
    "description": "This module is used to display extra fields on the Gantt view and the "
                   "popup is visible on the hover on the gantt.",
    "depends": ["web_gantt", "project_enterprise"],
    "data": [
        'views/web_gantt_templates.xml',
        'views/project_task_views.xml',
        #'views/project_task_image_field.xml',
        'views/custom_scss_gantt.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}