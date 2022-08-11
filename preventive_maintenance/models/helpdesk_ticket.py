from odoo import models, fields, api, _


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    notification_ids = fields.One2many('preventive_maintenance.notification','helpdesk_id', string="Notification IDs")
    high_skill_needed = fields.Boolean(string="High skill technician needed")

    system_ids = fields.One2many('preventive_maintenance.system',related='partner_id.system_ids')

