# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import logging

logger = logging.getLogger(__name__)


class ReorderingRuleTemplate(models.Model):
	_name = 'reordering.rule.template'
	_desc = 'Reordering rule template'

	name = fields.Char(string='Name')
	category_type = fields.Selection([('warehouse', 'Warehouse'), ('truck', 'Truck')], string='Impacted location type')
	location_ids = fields.One2many('stock.location', 'roerdering_rule_template_id', string='Locations list')
	category_ids = fields.One2many('stock.location.category', 'roerdering_rule_template_id', string='Categories list')

	reordering_rule_template_line_ids = fields.One2many('reordering.rule.template.line', 'roerdering_rule_template_id',
														string='Reordering Rule template lines')

	def update_location(self):
		reordering_obj = self.env['stock.warehouse.orderpoint']
		for loc in self.category_ids.mapped('location_ids'):
			recs = reordering_obj.search([('location_id', '=', loc.id)])
			recs.unlink()
			for line in self.reordering_rule_template_line_ids:
				reordering_obj.create({
					'product_id': line.product_id.id,
					'location_id': loc.id,
					'product_min_qty': line.product_min_qty,
					'product_max_qty': line.product_max_qty,
					'qty_multiple': line.qty_multiple,
				})


class ReorderingRuleTemplateLine(models.Model):
	_name = 'reordering.rule.template.line'
	_desc = 'Reordering rule template line'

	roerdering_rule_template_id = fields.Many2one('reordering.rule.template', string='Reordering rule template')
	product_id = fields.Many2one('product.product', string='Product')
	product_min_qty = fields.Float(string='Min Quantity')
	product_max_qty = fields.Float(string='Max Quantity')
	qty_multiple = fields.Float(string='Multiple Quantity')
