{
    'name': "Field Technician",
    'version': "14.0",
    'category': "Hidden",
    'depends': ['account', 'sale_project', 'stock', 'hr_expense', 'helpdesk'],
    'summary'
    'description': """
        field technician group 
    """,
    'author': 'Konsultoo',
    'website': 'http://www.konsultoo.com',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
    'auto_install': False
}
