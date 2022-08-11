# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import logging
logger = logging.getLogger(__name__)


class StockLocationCategory(models.Model):
	_name = 'stock.location.category'
	_desc = 'Location category'

	name = fields.Char(string='Category name')
	description = fields.Char(string='Description')
	category_type = fields.Selection([('warehouse','Warehouse'),('truck','Truck')], string='Location type')
	location_ids = fields.One2many('stock.location', 'category_id',string='Location list')
	roerdering_rule_template_id = fields.Many2one('reordering.rule.template', string='Reordering rule template')