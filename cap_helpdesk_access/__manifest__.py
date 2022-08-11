{
    'name': "Helpdesk Access",
    'version': "14.0",
    'category': "Hidden",
    'depends': ['sale_project', 'helpdesk','base'],
    'summary'
    'description': """
        helpdesk group 
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
