# -*- coding: utf-8 -*-
# from odoo import models, fields, api, _
# import logging
# logger = logging.getLogger(__name__)


# class ContactLocationRelationship(models.Model):
# 	_inherit = 'x_contact_location_rel'


# 	def createTicket(self):
# 		helpdesk = env['helpdesk.ticket'].create({
# 			'name':self.name,	
# 			'x_studio_customer_name':self.x_studio_contact.id,	
# 			'partner_id':self.x_studio_location.id,	
# 			'team_id':1,	
# 		})

# 		return {
# 				'type': 'ir.actions.act_window',
# 				'res_model': 'helpdesk.ticket',
# 				'view': 'helpdesk.helpdesk_ticket_view_form',
# 				'view_mode':'form',
# 				'res_id':helpdesk.id,
# 				'target': 'current',
# 		}

