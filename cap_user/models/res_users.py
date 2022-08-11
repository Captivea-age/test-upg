# -- coding: utf-8 --
from odoo import models, fields, api, _
from datetime import datetime, timedelta


class ResUsers(models.Model):
    _inherit = 'res.users'

    team_color = fields.Many2one('team.color', string="Team Color", store=True)
    technician_role = fields.Char(string="Technician role")
    color_id = fields.Integer(compute='_compute_color', store=True)
    technician_bool = fields.Boolean(string='Show in tech list')
    talkdesk_phone = fields.Char(string='Talkdesk phone number')
    today_less_8 = fields.Datetime(string='Today Less 8 Hours', compute='_compute_today_less_more_8')
    today_more_8 = fields.Datetime(string='Today Less 8 Hours', compute='_compute_today_less_more_8')

    def _compute_today_less_more_8(self):
        today = datetime.now()
        for record in self:
            record.today_less_8 = today - timedelta(hours=8)
            record.today_more_8 = today + timedelta(hours=8)

    @api.depends("team_color")
    def _compute_color(self):
        for rec in self:
            if rec.team_color.color:
                rec.color_id = rec.team_color.color


class ProjectTask(models.Model):
    _inherit = "project.task"

    team_color = fields.Integer(related="user_id.color_id")
    technician_team = fields.Many2one(related="user_id.employee_id.department_id", string="Team", store=True)
