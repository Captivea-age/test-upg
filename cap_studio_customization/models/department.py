# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class Department(models.Model):
    _name='cap.department'
    _description = 'Department'
    _order = 'sequence asc, id asc'

    name = fields.Char(string='Name')
    active = fields.Boolean('Active')
    sequence = fields.Integer(string='Sequence')
