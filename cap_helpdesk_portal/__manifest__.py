# -*- coding: utf-8 -*-

{
    "name": "Cap Helpdesk Portal",
    "version": "1.0",
    'author': "Captivea",
    'website': "www.captivea.us",
    "category": "Helpdesk",
    "description": "This module is used to open a helpdesk record link "
                   "and assign a location with close the ticket or open a ticket.",
    "depends": ["helpdesk"],
    "data": [
        'views/approval_helpdesk_ticket.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
