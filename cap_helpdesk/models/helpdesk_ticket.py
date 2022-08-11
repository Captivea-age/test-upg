# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import logging
logger = logging.getLogger(__name__)


class HelpdeskTicket(models.Model):
	_inherit = 'helpdesk.ticket'

	authority = fields.Boolean(string='Authority over closure', default=True)
	customer_closure_approval = fields.Boolean(string='Customer approval for closure')


	_1st_approval_sent =  fields.Boolean(string='1st approval sent')
	_2nd_approval_sent =  fields.Boolean(string='2nd approval sent')
	_3rd_approval_sent =  fields.Boolean(string='3rd approval sent')
	_4th_approval_sent =  fields.Boolean(string='4th approval sent')

	followup_notes = fields.Text(string="Followup notes")
	followup_department = fields.Many2many('followup.department',string='Followup department')

	approval_link = fields.Char(string="Approval link",compute="_compute_approval_link")

	display_error = fields.Char(compute='_compute_display_error',stored='False')
	display_warning = fields.Char(compute='_compute_display_warning',stored='False')
	display_info = fields.Char(compute='_compute_display_info',stored='False')

	system_ids = fields.One2many('preventive_maintenance.system',related='partner_id.system_ids')


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



	def _compute_approval_link(self):
		url = self.env['ir.config_parameter'].get_param('web.base.url')
		self['approval_link'] = str(url)+"/approval/"+str(self.id)
		return True


	def createContact(self):

		context = {			
			'default_partner_type':'person',
			'default_helpdesk_id':self.id,	
			'default_street':self.partner_id.street,   
			'default_street2':self.partner_id.street2,   
			'default_city':self.partner_id.city,   
			'default_zip_code':self.partner_id.zip,   
		}
		view_form = self.env.ref('cap_helpdesk.view_helpdesk_ticket_partner', False)

		return {
			'type' : 'ir.actions.act_window',
			'name' : 'New contact',
			'res_model': 'helpdek.ticket.partner',
			'views': [(view_form.id,'form')],
			'view_mode':'form',
			'view_type':'form',
			'context':context,
			'target': 'new',
		}



	def createLocation(self):

		context = {			
			'default_partner_type':'location',	   
			'default_location_type_id':1,
			'default_helpdesk_id':self.id	   
		}		

		return {
			'type' : 'ir.actions.act_window',
			'name' : 'New location',
			'res_model': 'helpdek.ticket.partner',
			
            'views': [[self.env.ref('cap_helpdesk.view_helpdesk_ticket_partner').id,'form']],
			'view_mode':'form',
			'view_type':'form',
			'context':context,
			'target': 'new',
		}

	def openSystemCreation(self):
		context = {
			'default_location_id':self.partner_id.id,
			'default_helpdesk_ticket_id':self.id,
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

class HelpdeskTicketPartner(models.Model):
	_name = 'helpdek.ticket.partner'

	name = fields.Char(string='Name')
	street = fields.Char(string='Street')
	street2 = fields.Char(string='Street2')
	city = fields.Char(string='City')
	zip_code = fields.Char(string="ZIP")
	country_id = fields.Many2one('res.country', string="Country")
	state_id = fields.Many2one('res.country.state', string="Country")
	phone = fields.Char(string='Landline')
	email = fields.Char(string='email')
	current_partner_id = fields.Many2one('res.partner',string='Current partner')
	same_address = fields.Boolean(string='Use same street')
	partner_type = fields.Selection([('person', 'Person'), ('company', 'Company'), ('location', 'Location')], string='Record Type')


	relationship_type = fields.Selection([('Resident Owner','Resident owner'),('Tenant','Tenant'),('Property Manager','Property manager'),('Landlord','Landlord'),('Other Contact','Other Contact')],string='Relationship type')
	contact_roles = fields.Many2many('contact.role',string='Contact roles')
	contact_method = fields.Many2many('contact.method',string='Contact methods')

	location_type_id =  fields.Many2one('location.type',string="Location type")

	helpdesk_id = fields.Many2one('helpdesk.ticket',string="Helpdesk Ticket ID")

	def savePartner(self):

		partner = self.env['res.partner'].create({
			'name':self.name,	
			'street':self.street,	
			'street2':self.street2,	
			'city':self.city,	
			'state_id':self.state_id.id,
			'zip':self.zip_code,	
			'country_id':self.country_id.id,	
			'phone':self.phone,	
			'email':self.email,
		})

		self['current_partner_id'] = partner.id
		logger.info('Created partner %s', partner.name)


		#Instead of creating, we use the location set in the helpdesk ticket

		location = self.helpdesk_id.partner_id
		if self.same_address and self.partner_type != 'location' : 

			contact = self.current_partner_id

		# 	location = self.env['res.partner'].create({
		# 		'name':self.street,	
		# 		'street':self.street,	
		# 		'street2':self.street2,	
		# 		'city':self.city,	
		# 		'state_id':self.state_id.id,
		# 		'zip':self.zip_code,	
		# 		'country_id':self.country_id.id,	
		# 	})

			relation = self.env['contact.location.relationship'].create({
				'name':('%s - %s - %s ' % (str(contact.name),str(location.name),str(self.relationship_type))),
				'contact_id':contact.id,
				'location_id':location.id,
				'relationship_type':self.relationship_type,
				'pick_a_location':'Existing Location',
				'preferred_contact_method_ids':[1,2,3],
				'contact_roles_ids':[1,2],

			})

		# We don't need to update the ticket anymore 

#	self.helpdesk_id.write({
#			'partner_id':relation.location.id,
#			'customer_name':relation.contact.id,
#			'pick_the_location':relation.id,
#			'city':relation.location_city,
#			'zip':relation.location_zip,
#	})

			return {
				'type': 'ir.actions.act_window',
				'res_model': 'helpdesk.ticket',
				'view': 'helpdesk.helpdesk_ticket_view_form',
				'view_mode':'form',
				'res_id':self.helpdesk_id.id,
				'target': 'current',
			}

		return {
			'type' : 'ir.actions.act_window',
			'name' : '',
			'res_model': 'helpdek.ticket.partner',
			'views': [[self.env.ref('cap_helpdesk.view_helpdesk_ticket_partner').id,'form']],
			'view_mode':'form',
			'view_type':'form',
			'res_id':self.id,
			'target': 'new',
		}



	def openLocationPopup(self):

		context = {
			'default_location_diff':'=',
			'default_current_partner_id':self.current_partner_id.id,
			'default_relationship_type':'Resident Owner',
			'default_helpdesk_ticket_id':self.helpdesk_id.id
		}

		return {
				'type': 'ir.actions.act_window',
				'res_model': 'search.popup',
				'view': 'view.res.partner.search.popup',
				'view_mode':'form',
				'context':context,
				'target': 'new',
			}

	def openContactPopup(self):

		context = {
			'default_location_diff':'!=',
			'default_current_partner_id':self.current_partner_id.id,
			'default_relationship_type':'Resident Owner',
			'default_helpdesk_ticket_id':self.helpdesk_id.id
		}

		return {
				'type': 'ir.actions.act_window',
				'res_model': 'search.popup',
				'view': 'view.res.partner.search.popup',
				'view_mode':'form',
				'context':context,
				'target': 'new',
			}