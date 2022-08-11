# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
	_inherit = 'sale.order.line'

	system_id = fields.Many2one('preventive_maintenance.system',string='System')
	location_id = fields.Many2one('res.partner',related='order_id.partner_id',string='System')