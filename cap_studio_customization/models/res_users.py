# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ResUsers(models.Model):
    _inherit='res.users'

    show_in_job_technician_list = fields.Boolean(string='Show in Job Technician List')
