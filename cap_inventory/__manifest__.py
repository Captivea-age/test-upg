{
    'name': 'Inventory customizations',
    'version': '1.1',
    'author': "Abdessamad GERARD @ Captivea",
    'website': 'www.captivea.us',
    'category': 'Website',
    'summary': 'Inventory customizations module; Stores all new changes on the module..',
    'description': """
    Inventory customizations module; Stores all new changes on the module.
       """,
    'depends': ['base','stock','web_studio'],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_location_custom.xml',
        'views/reordering_rule_template.xml',
        'views/reordering_rule_template_line.xml',
        'views/actions_and_menu.xml',
        'views/product_template_custom.xml',
        'views/product_template_attribute_value.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
