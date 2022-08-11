# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class Notification(models.Model):

    _name = "preventive_maintenance.notification"
    _description = "Notification records"

    name = fields.Char(string="Name")
    location_id = fields.Many2one("res.partner", string="Location")
    system_id = fields.Many2one("preventive_maintenance.system", string="System")
    inspection_time_needed = fields.Float(string="Total Time needed")
    high_skill_time_needed = fields.Float(string="High skill Time needed")
    low_skill_time_needed = fields.Float(string="Low skill Time needed")
    risk_score = fields.Float(string="Risk score")
    inspection_ids = fields.One2many("preventive_maintenance.maintenance","notification_id",string="Inspection records")
    dashboard_id = fields.Many2one("preventive_maintenance.notification.dashboard", string="Dashboard ID")
    notification_status = fields.Selection([('none','None'),('pending','Pending'),('sent','Sent'),('dismissed','Dismissed'),('scheduled','Scheduled')],string="Notification status",default="none")
    helpdesk_id = fields.Many2one('helpdesk.ticket',string="Helpdesk ticket")

    def createTicket(self):
#Ticket creation
        high_skill_needed = False
        location = self.location_id
        maintenance_team = self.env['helpdesk.team'].search([('name','=','Maintenance')],limit=1)

        # Get other notifications
        notifications = self.env['preventive_maintenance.notification'].search([('location_id','=',location.id),('notification_status','=','none')])

        time = 0
        for notification in notifications:
            time += notification.inspection_time_needed
            notification.system_id['notification_status'] = 'sent'
            if notification.high_skill_time_needed > 0:
                high_skill_needed = True

        #Loking for existing ticket
        ticket = self.env['helpdesk.ticket'].search([('partner_id','=',location.id),
        ('stage_id','not in',[9,10,15,16,21,24,25]),
        ('notification_ids','in',self.id)],
        limit=1,
        order="id desc")

        if len(ticket) == 0:
            ticket = self.env['helpdesk.ticket'].create({
                'name':'Inspection request :'+str(location.name),
                'team_id': maintenance_team.id,
                'partner_id':location.id,
                'kanban_state':'normal',
                'x_studio_time_needed':time,
                'high_skill_needed':high_skill_needed,
            })
        for notification in notifications:
            notification['notification_status'] = 'sent'
            notification['helpdesk_id']=ticket.id


#### Email and SMS notification
        relationship = self.env['x_contact_location_rel'].search([('x_studio_location','=',location.id),('x_studio_contact_roles','in',1)], limit=1)
        owner = relationship.x_studio_contact
        subject = "Maintenance is required on your systems"
        message = "Hello "+str(owner.name)+". The MonsterShield has detected that at least one of your system requires a preventive maintenance. Please reach out to us to schedule an intervention. Best regards, from ComfortMonster."



        for contact_method in relationship.x_studio_preferred_contact_method:
            if contact_method.id == 1 :
                if owner.email:
                    template_obj = self.env['mail.mail']
                    template_data = {
                          'subject': subject,
                          'body_html': message,
                          'email_from': "MonsterShield@comfortmonster.odoo.com",
                          'email_to': owner.email,
        #                  'model':'hr.employee',
        #                  'res_id':id,
                          }

                    template_id = template_obj.create(template_data)
                    template_id.send()


            if contact_method.id == 2:
                if owner.mobile :
                  sms = self.env['wk.sms.sms'].create({
                    'group_type':'individual',
                    'partner_id':owner.id,
                    'sms_gateway_config_id':1,
                    'to':owner.mobile,
                    'auto_delete':False,
                    'template_id':1,
                    'msg':message
                  })

                  sms.send_now()






        return {
                'type': 'ir.actions.act_window',
                'res_id':ticket.id,
                'view_mode': 'form',
                'res_model': 'helpdesk.ticket',
                'views': [(False, 'form')],
                'view_id': False,
                'target': 'current',
            }
