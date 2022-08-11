# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
_logger = logging.getLogger(__name__)


class ProductTemplateAttributeValue(models.Model):
	_inherit = 'product.template.attribute.value'

	cost = fields.Float(string="Cost")