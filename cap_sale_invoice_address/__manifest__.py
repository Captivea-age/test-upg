# -*- coding: utf-8 -*-

{
    "name": "Sales order Invoice address correction",
    "version": "0.2",
    'author': "Abdessamad GERARD @ Captivea",
    'website': "www.captivea.us",
    "category": "Fleet",
    "description": "Updates correctly the invoice address when sale order is created from Task",
    "depends": [
        "base",
        "sale",
        "sale_management",
        "project",
    ],
    "data": [
        "security/ir.model.access.csv",
        'security/security.xml',
        'views/quotation_template.xml'
    ],
    'installable': True,
    'application': True,
}
