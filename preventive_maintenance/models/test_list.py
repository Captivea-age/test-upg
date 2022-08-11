# -- coding: utf-8 --
from odoo import models, fields, api, _
from datetime import date, datetime, timedelta
import logging
logger = logging.getLogger(__name__)

class TestList(models.Model):
	_name = "pm.test.list"
	_description = "Set of tests that can be created"

	name = fields.Char(string='Tests list name')
	#test_ids = fields.One2many('preventive_maintenance.test.category','test_list_ids',string='Linked Tests list')
	
class TestListPopup(models.TransientModel):
		_name = 'pm.test.list.popup'

		name = fields.Char(string='Name')
		test_list_id = fields.Many2one('pm.test.list', string="Test list to generate")
		job_id = fields.Many2one('project.task', string="Job #")
		system_id = fields.Many2one('preventive_maintenance.system', string="System")



			
		def generateList(self):
			test_object = self.env['preventive_maintenance.test.category']

			test_object.testCreation(test_list=self.test_list_id,system_id=self.system_id,job_id=self.job_id)

			return {
			  'type': 'ir.actions.act_window_close'
			}
