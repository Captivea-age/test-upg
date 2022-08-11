# -*- coding: utf-8 -*-
{
    'name': "SW - Sale Order From Multiple Warehouses",
    'summary': """Allows multiple deliveries from multiple warehouses in a single sale order""",
    'author': "Smart Way Business Solutions",
    'website': "https://www.smartway.co",
    'license':  "Other proprietary",
    'category': 'Sales',
    'version': '1.0',
    'depends': ['base', 'sale', 'stock', 'sale_stock'],
    'data': [
        'views/sale_order_views.xml',
    ],
    'images':  ["static/description/image.png"],
    'price'    :  160,
    'currency' :  'EUR',
    'installable': True,
}
