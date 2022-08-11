# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    date_today = fields.Date(compute='_compute_date_today')

    def _compute_date_today(self):
        for user in self:
            user.date_today = fields.Date.today()


