

from odoo import models, fields, api, _


class Maintenance(models.Model):

    _name = "preventive_maintenance.maintenance"
    _description = "Inspection records model"

    name= fields.Char(string="Name")
    system_id = fields.Many2one("preventive_maintenance.system", string="System")
    notification_id = fields.Many2one("preventive_maintenance.notification", string="Notification")
    job_id = fields.Many2one("project.task", string="Job")
    date = fields.Date(string="Date")
    pm_type = fields.Selection([('post_install_pm','Post Install'),('winter_pm','Winter PM'),('summer_pm','Summer PM'),('inspection_pm','Inspection PM'),('certified_pm','Certified Inspection PM')],string="PM Type")
    state = fields.Selection([('good','Good'),('warning','Warning'),('error','Error')], string="System Health")
    tests_done = fields.One2many("preventive_maintenance.test.records","maintenance_id", string="Test results")
