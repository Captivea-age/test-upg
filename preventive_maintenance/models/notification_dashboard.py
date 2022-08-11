from odoo import models, fields, api, _

class NotificationDashboard(models.Model):

    _name = "preventive_maintenance.notification.dashboard"
    _description = "Notification dashboard"

    name = fields.Char(string="Name",default="Notification Dashboard")
    high_skill_available = fields.Float(string="High skill time available")
    low_skill_available = fields.Float(string="Low skill time available")
    risk_treshold = fields.Float(string="Risk treshold")
    pm_type = fields.Selection([('post_install_pm','Post Install'),('winter_pm','Winter PM'),('summer_pm','Summer PM'),('inspection_pm','Inspection PM'),('certified_pm','Certified Inspection PM')],string="PM Type")

    notification_ids = fields.One2many("preventive_maintenance.notification","dashboard_id",string="Notification records")
    filtered_notification_ids = fields.One2many("preventive_maintenance.notification", string="Notification records", compute='_get_filtered_notif_ids', readonly=False)

    @api.onchange('notification_ids')
    def _get_filtered_notif_ids(self):
        if self.notification_ids:
            self.filtered_notification_ids = self.notification_ids.filtered(lambda notif: notif.notification_status == 'none')
