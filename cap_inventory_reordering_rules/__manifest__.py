{
    'name': 'Cap Inventory Reordering Rules',
    'version': '1.0',
    'author': "Captivea",
    'website': 'www.captivea.us',
    'category': 'Website',
    'summary': 'Generating reordering rules from wizard.',
    'description': """
    This module provides creating reordering rules for multiple products with multiple locations.
       """,
    'depends': ['stock'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/inventory_order_point_view.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
