# -- coding: utf-8 --
from odoo import models, fields, api, _
import logging
logger = logging.getLogger(__name__)


class InternalAlert(models.Model):
	_name = 'internal.alert'
	_description = 'Internal alerts for res.partners'

	partner_id = fields.Many2one('res.partner',string='Partner')
	alert_level = fields.Selection([('info','Info'),('warning','Warning'),('error','Error')], string='Alert level')
	alert_text = fields.Char(string='Alert text')
	alert_active = fields.Boolean(string='Active ?', default=True)


class ResPartner(models.Model):
	_inherit = 'res.partner'

	alert_ids = fields.One2many('internal.alert','partner_id',string='Alert list')
	display_error = fields.Char(compute='_compute_display_error',store='False')
	display_warning = fields.Char(compute='_compute_display_warning',store='False')
	display_info = fields.Char(compute='_compute_display_info',store='False')

	def _compute_display_error(self):
		for record in self:
			start = "<div>"
			text = ""
			end = "</div>"
			results = record.env['internal.alert'].search([('partner_id','=', record.id),('alert_level','=','error'),('alert_active','=',True)])
			for result in results:
				text += "<p>"" - "+result.alert_text+"</p>"

			record['display_error'] = start + text + end
			return True

	def _compute_display_warning(self):
		for record in self:
			start = "<div>"
			text = ""
			end = "</div>"
			results = record.env['internal.alert'].search([('partner_id','=',record.id),('alert_level','=','warning'),('alert_active','=',True)])
			for result in results:
				text += "<p>"" - "+result.alert_text+"</p>"

			record['display_warning'] =  start + text + end
			return True

	def _compute_display_info(self):
		for record in self:
			start = "<div>"
			text = ""
			end = "</div>"
			results = record.env['internal.alert'].search([('partner_id','=',record.id),('alert_level','=','info'),('alert_active','=',True)])
			for result in results:
				text += "<p>"" - "+result.alert_text+"</p>"

			record['display_info'] =  start + text + end
			return True

	def openAlertPopup(self):
		context = {
			'default_partner_id':self.id,
		}
		logger.info('Tried to open the alert popup')

		return {
				'type': 'ir.actions.act_window',
				'res_model': 'internal.alert',
				'view': 'view.internal.alert.form',
				'view_mode':'form',
				'context':context,
				'target': 'new',
		}
