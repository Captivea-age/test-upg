from odoo import models, fields, api, _
import datetime
import requests
import json
import base64
import logging
logger = logging.getLogger(__name__)

class ProjectTask(models.Model):
    _inherit = "project.task"

    # fields added from studio
    helpdesk_tag_ids = fields.Many2many('helpdesk.tag', 'helpdesk_tag_project_task_rel', 'tag_id', 'task_id', string='Tags')
    # tag_ids = fields.Many2many('helpdesk.tag', 'helpdesk_tag_project_task_rel_1', 'tag_id', 'task_id',string='Tags')
    pick_the_location_id = fields.Many2one('contact.location.relationship', string='Pick the location')
    customer_name = fields.Many2one('res.partner', string='Customer Name', related='pick_the_location_id.contact_id')
    location_id = fields.Many2one('res.partner', string='Location', ondelete='set null',related='partner_id', copy=True, store=True)
    street1 = fields.Char(related='partner_id.street', string='Street', stored=False)
    street2 = fields.Char(related='partner_id.street2', string='Street2', stored=False)
    city = fields.Char(related='partner_id.city', string='City', stored=False)
    state = fields.Char(related='partner_id.state_id.name', string='State', stored=False)
    zip = fields.Char(related='partner_id.zip', string='Zip', stored=False)
    country_id = fields.Many2one('res.country', related='partner_id.country_id', string='Country', stored=False)
    # End of studio fields

    schedule_ready = fields.Boolean(string="Schedule ready ?")
    send_notification = fields.Boolean(string="Send notification ?", default="True")
    notification_sent = fields.Boolean(string="Notification sent ?", readonly="True")
    start_date = fields.Date(string="Start date")
    planned_hour_start = fields.Many2one("time.selection",string="Planned start hour")
    planned_hour_end = fields.Many2one("time.selection",string="Planned end hour")
    x_followers_already_wiped = fields.Boolean(string="Followers already wiped", default="False")
    arrival_window = fields.Many2one("arrival.window",string="Arrival window")
    phone_numbers_ids = fields.One2many(related="customer_name.phone_number_ids")
    followup_needed = fields.Boolean(string='Followup needed ?')
    followup_department = fields.Many2many('followup.department',string='Followup department')
    followup_notes = fields.Char(string='Followup notes')
    global_info_bar = fields.Char(string="Info bar",stored=False,compute="_compute_info_bar")
    global_warning_bar = fields.Char(string="Warning bar",stored=False,compute="_compute_warning_bar")
    global_error_bar = fields.Char(string="Alert bar",stored=False,compute="_compute_error_bar")
    all_contact_info = fields.Char(string="Contact information",compute="_computeAllContactInfo")
    service_titan_id = fields.Integer(string="ST ID")
    service_titan_link = fields.Char(string="ST link", compute='_computeSTLink',stored=False)

    display_error = fields.Char(compute='_compute_display_error',stored=False)
    display_warning = fields.Char(compute='_compute_display_warning',stored=False)
    display_info = fields.Char(compute='_compute_display_info',stored=False)
    
    partner_age = fields.Char(related="partner_id.partner_age",string='Partner age')
    monstercare_member = fields.Boolean(related="partner_id.monstercare_member",string='Monstercare member', default="False")

    material_list_ids = fields.Many2many('sale.order.line',string='Materials', compute='_compute_material_list_ids', stored="False")
    
    def action_fsm_navigate(self):
        if not self.partner_id.partner_latitude and not self.partner_id.partner_longitude:
            self.partner_id.geo_localize()
        # YTI TODO: The url should be set with single method everywhere in the codebase
#         url = "https://www.google.com/maps/dir/?api=1&destination=%s,%s" % (self.partner_id.partner_latitude, self.partner_id.partner_longitude)
        url = "https://www.google.com/maps/dir/?api=1&destination=%s,%s" % (self.partner_id.street, self.partner_id.city)
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new'
        }

    def _computeSTLink(self):
        self.update({
            'service_titan_link' :'<a href="https://go.servicetitan.com/#/Job/Index/'+str(self.service_titan_id)+'" target="_blank">ServiceTitan Job</a>'
        })

    def _compute_material_list_ids(self):
        sales = self.env['sale.order'].search([('task_id','=',self.id)])
        material_ids = []
        for sale in sales:
            for line in sale.order_line:
                if line.product_id.type == 'product':
                    material_ids.append(line.id)

        self.update({
            'material_list_ids':[(6, 0, material_ids)]
        })

        return True

    def openMaterialPopup(self):
        context = {
            'fsm_task_id': self.id,
            'default_product_category_id': False,
        }
        popup = self.env['material.popup'].search([('task_id','=',self.id)])

        if len(popup) > 0:
                res_id = popup.id
        else:
            popup = self.env['material.popup'].create({
                'task_id':self.id,
            })
            res_id = popup.id

        return {
            'type' : 'ir.actions.act_window',
            'name' : 'Material',
            'res_model': 'material.popup',
            'res_id':popup.id,
            'views': [[self.env.ref('cap_field_service.material_popup_form_view').id,'form']],
            'view_mode':'form',
            'view_type':'form',
            'context':context,
            'target': 'new',
        }

    # talkdeskPhoneNumber = '+19195825914'
    # talkdeskPhoneNumber = fields.Char(related='user_id.talkdesk_phone',string="Talkdesk phone number")
    # contactPhoneNumber = '+18009199835'
    clientId = '81d2fb0ebd1d48f5b659fe1217ca6861'
    clientSecret = 'KduB_hnT7YuLz7Mk8aZamCyJzBGhHOMKeM0fik1laRiLHcoEUkFl1NGoLpU2BUq8i3f-OxESNECv6vj_PvnJMA'


    def callContact(self,contactPhoneNumber):
        message = self.clientId + ':' + self.clientSecret
        messageBytes = message.encode('ascii')
        base64Bytes = base64.b64encode(messageBytes)
        token = base64Bytes.decode('ascii')
        auth = getAuth(token)
        authData = json.loads(auth.text)
        response = getCallback(authData['access_token'], self.user_id.talkdesk_phone, contactPhoneNumber)
        logger.warning(print(response.text))


    def getAuth(token):
        url = 'https://comfortmonsterco.talkdeskid.com/oauth/token'
        myobj = {
            'grant_type': 'client_credentials',
            'scope': 'callback:write'
        }
        headers = {
            'Authorization': 'Basic ' + token,
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        return requests.post(url, data = myobj, headers = headers)


    def getCallback(accessToken, talkdeskPhoneNumber, contactPhoneNumber,contactName):
        url = 'https://api.talkdeskapp.com/calls/callback'
        context = {}
        fields = {}
        context = {}
        fields = [
            {
                "data_type": "text",
                "display_name": contactName,
                "name": contactName,
                "tooltip_text": "The name of the customer, as inserted in our website",
                "value": contactName
            },
            {
                "data_type": "url",
                "display_name": "Current page",
                "name": "current_page",
                "tooltip_text": "The last visited page of the customer on our website",
                "value": "https://example.com/"
            }
        ]
        context['fields'] = fields
        myobj = {
            'talkdesk_phone_number':  self.user_id.talkdesk_phone,
            'contact_phone_number': contactPhoneNumber,
            'context': context
        }
        headers = {
            'Authorization': 'Bearer ' + accessToken,
            'Content-Type': 'application/json',
        }
        return requests.post(url, json = myobj, headers = headers)

    def _compute_display_error(self):
        for record in self:
            start = "<div>"
            text = ""
            end = "</div>"
            results = record.env['internal.alert'].search(['|',('partner_id','=',record.partner_id.id),('partner_id','=',record.customer_name.id),('alert_level','=','error'),('alert_active','=',True)])
            for result in results:
                text += "<p>"" - "+result.alert_text+"</p>"

            record['display_error'] = start + text + end
            return True

    def _compute_display_warning(self):
        for record in self:
            start = "<div>"
            text = ""
            end = "</div>"
            results = record.env['internal.alert'].search(['|',('partner_id','=',record.partner_id.id),('partner_id','=',record.customer_name.id),('alert_level','=','warning'),('alert_active','=',True)])
            for result in results:
                text += "<p>"" - "+result.alert_text+"</p>"

            record['display_warning'] =  start + text + end
            return True

    def _compute_display_info(self):
        for record in self:
            start = "<div>"
            text = ""
            end = "</div>"
            results = record.env['internal.alert'].search(['|',('partner_id','=',record.partner_id.id),('partner_id','=',record.customer_name.id),('alert_level','=','info'),('alert_active','=',True)])
            for result in results:
                text += "<p>"" - "+result.alert_text+"</p>"

            record['display_info'] =  start + text + end
            return True

    def _computeAllContactInfo(self):
        text = "<div>"
        for relationship in self.partner_id.contact_list_ids:
            text += "<b>"+str(relationship.contact_id.name)+" - "+str(relationship.relationship_type)+"</b><br/>"
            if relationship.contact_phone:
#                 text += str(relationship.contact_phone)+"<button icon='fa-phone' class='btn btn-primary' name='callContact("+str(relationship.contact_phone)+")' string='Call' type='object'></button>"
                text += "<a href='tel:"+str(relationship.contact_phone)+"'>"+str(relationship.contact_phone)+"</a>"
            else:
                text += "No phone."
            text += "<br/>"
            
            if relationship.contact_mobile:
#                 text += str(relationship.contact_mobile)+"<button icon='fa-phone' class='btn btn-primary' name='callContact("+str(relationship.contact_mobile)+")' string='Call' type='object'></button>"
                text += "<a href='tel:"+str(relationship.contact_mobile)+"'>"+str(relationship.contact_mobile)+"</a>"
            else:
                text += "No mobile."
            text += "<br/>"

            if relationship.contact_email:
                # text += "<a href='mailto:"+str(relationship.contact_email)+"'>"+str(relationship.contact_email)+"</a><br/>"
                 text += str(relationship.contact_email)
            else:
                text += "No email."
            text += "<br/><br/>"
            
        text += "</div>"

        self['all_contact_info'] = text
        
        return self['all_contact_info']


    def getAllMessagesFromContact(self,message_type):
        text = "<ul>"
        for relationship in self.partner_id.contact_list_ids:
            for alert in relationship.contact_id.alert_ids.filtered(lambda x: x.alert_level == message_type):
                text += "<li>"+alert.alert_text+"</li>"
        text += "</ul>"
        return text

    def _compute_info_bar(self):
        self['global_info_bar'] = self.getAllMessagesFromContact('Info')
        
        return self['global_info_bar']

    def _compute_warning_bar(self):
        self['global_warning_bar'] = self.getAllMessagesFromContact('Warning')
        
        return self['global_warning_bar']

    def _compute_error_bar(self):
        self['global_error_bar'] = self.getAllMessagesFromContact('Error')
        
        return self['global_error_bar']
    
    def openSystemCreation(self):
        context = {
            'default_location_id':self.partner_id.id,
            'default_notification_status':'none',
        }
        
        return {
            'type' : 'ir.actions.act_window',
            'name' : 'New system',
            'res_model': 'preventive_maintenance.system',
            'views': [[self.env.ref('preventive_maintenance.view_pm_system_form').id,'form']],
            'view_mode':'form',
            'view_type':'form',
            'context':context,
            'target': 'new',
        }
        
class FollowupDepartment(models.Model):
    _name = 'followup.department'
    _description = 'Followup Department'

    name = fields.Char(string="Department name")
    description = fields.Char(string="Department description")
