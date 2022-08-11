# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    task_id = fields.Many2one('project.task', compute='_compute_task', string='Job')
    
    def _compute_task(self):
        order = False
        for record in self:
            if record.invoice_line_ids:
                for invoice_line in record.invoice_line_ids:
                    if invoice_line.sale_line_ids:
                        for sale_line in invoice_line.sale_line_ids:
                            if sale_line.order_id:
                                order = sale_line.order_id
                                break
            if order:
                if order.task_id:
                    record['task_id'] = order.task_id


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    product_visible_on_customer_invoice = fields.Boolean(related='product_id.visible_on_customer_invoice', string='Product Visible on Customer Invoice')
