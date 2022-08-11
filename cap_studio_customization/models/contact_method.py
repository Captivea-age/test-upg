# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ContactMethod(models.Model):
    _name='contact.method'
    _description = 'Contact Method'
    _order = 'sequence asc, id asc'

    name = fields.Char(string='Name')
    active = fields.Boolean('Active')
    sequence = fields.Integer(string='Sequence')
