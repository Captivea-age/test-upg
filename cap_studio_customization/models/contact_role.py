# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ContactRole(models.Model):
    _name='contact.role'
    _description = 'Contact Role'
    _order = 'sequence asc, id asc'

    name = fields.Char(string='Name')
    active = fields.Boolean('Active')
    sequence = fields.Integer(string='Sequence')
