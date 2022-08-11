# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class QuotationTemplate(models.Model):
    _inherit = 'sale.order.template'

    deposit_invoice_automation = fields.Boolean(string='Automated deposit')
    deposit_dollar = fields.Float(string='Deposit $')
    deposit_percentage = fields.Float(string='Deposit %')

