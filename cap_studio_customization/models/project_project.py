# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ProjectProject(models.Model):
    _inherit = 'project.project'

    job_link_1 = fields.Many2one('project.task', related='sale_order_id.task_id', string='Job Link', store=True, ondelete='set null', help='Task from which quotation have been created')
    helpdesk_ticket = fields.Many2one('helpdesk.ticket', related='sale_order_id.helpdesk_ticket_id', string='Helpdesk Ticket', store=True)
