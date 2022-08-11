# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import logging
logger = logging.getLogger(__name__)


class StockLocation(models.Model):
	_inherit = 'stock.location'

	name = fields.Char(string='Category name')
	description = fields.Char(string='Category description')
	
	category_id = fields.Many2one('stock.location.category', string='Category')
	roerdering_rule_template_id = fields.Many2one('reordering.rule.template', string='Reordering rule template')
	reordering_rule_list = fields.One2many('stock.warehouse.orderpoint', 'location_id', string='Reordering rules list')
