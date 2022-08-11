# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class HelpdeskTag(models.Model):
    _inherit = 'helpdesk.tag'

    emoji = fields.Binary(string='Emoji')
    emoji_filename = fields.Char(string='Filename')
    priority = fields.Boolean(string="Priority")
