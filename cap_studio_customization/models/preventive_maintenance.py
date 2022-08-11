# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class PreventiveMaintenanceSystem(models.Model):
    _inherit = 'preventive_maintenance.system'

    accessories_ids = fields.Many2many('pm.accessories.component', 'pm_accessories_component_preventive_maintenance_system_rel', 'pm_accessories_component_id', 'preventive_maintenance_system', string='Accessories Model')
    equipment_id = fields.Many2one('cap.equipment', string='Equipment', ondelete='set null')
    subscription_id = fields.Many2one('sale.subscription', string='Subscription', ondelete='set null')
    system_location_id = fields.Many2one('preventive_maintenance.system_location', string='System Location', ondelete='set null')
    service_area_custom = fields.Char(string='Service Area Custom')


class NotificationDashboard(models.Model):
    _inherit = "preventive_maintenance.notification.dashboard"
    
    notifications_cleaned = fields.Html(compute='_compute_notifications_cleaned', string='Notifications Cleaned', store=True)

    @api.depends('notification_ids')
    def _compute_notifications_cleaned(self):
        for record in self:
            table = ""
            # previous_location = False
            # if len(record['notification_ids'])>0:
            #     header = '<div id="notifications"><div>'
            #     body = ''
            #     for notification in record['notification_ids'].sorted(lambda n:n.location_id).sorted(lambda n: n.risk_score, reverse=True):
            #         if notification.location_id.name != previous_location:
            #             body += '</div><div class="card"><div class="card-header" id="'+str(notification.location_id.id)+'" >'
            #             body += '<h4 class="mb-0"><button string="'+str(notification.location_id.name)+'" data-toggle="collapse" data-target="#collapse'+str(notification.location_id.id)+'" aria-expanded="true" aria-controls="collapse'+str(notification.location_id.id)+'">'+str(notification.location_id.name)+'</button> - <button class="btn btn-primary" string="Create inspection" name="create_helpdesk" type="object"></button></h4></div>'
                        
            #             previous_location = notification.location_id.name

            #         body += '<div id="collapse'+str(notification.location_id.id)+'" aria-labelledby="heading'+str(notification.location_id.id)+'" class="collapse show" data-parent="#notifications"><div class="card-body"><table><tr><th>System name</th><th>Total time needed</th><th>High skill</th><th>Low skill</th><th>Risk score</th></tr><tr><td>'+str(notification.system_id.name)+'</td><td>'+str(notification.inspection_time_needed)+'</td><td>'+str(notification.high_skill_time_needed)+'</td><td>'+str(notification.low_skill_time_needed)+'</td><td>'+str(notification.risk_score)+'</td></tr></table></div></div>'
            #         footer = '</div>'
            #         table = header+body+footer
            record['notifications_cleaned'] = table


class TestRecord(models.Model):
    _inherit = "preventive_maintenance.test.records"

    test_category_1 = fields.Char(related='test_type.test_type_id.display_name', string='Test Category 1')
    test_category = fields.Char(related='test_type.test_type_id.display_name', string='Test Category')
