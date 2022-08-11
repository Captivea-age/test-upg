# -*- coding: utf-8 -*-
{
    'name': "Cap - Sale Order Custom",
    'summary': """Custom Sales Order""",
    'author': "Thomas PETITHORY @ Captivea",
    'website': "",
    'license':  "Other proprietary",
    'category': 'Sales',
    'version': '1.2',
    'depends': ['base', 'sale','preventive_maintenance'],
    'data': [
        'views/sale_order_views.xml',
        'views/sale_order_line_views.xml',
        'views/invoice_views.xml',
    ],
    'images':  ["static/description/image.png"],
    'installable': True,
}
