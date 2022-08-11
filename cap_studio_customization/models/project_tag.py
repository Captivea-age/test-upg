# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ProjectTags(models.Model):
    _inherit = 'project.tags'

    image = fields.Binary(string='Image', store=True)