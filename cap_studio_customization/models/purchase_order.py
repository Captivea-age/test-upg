# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class PurchaseOrder(models.Model):
    _inherit='purchase.order'

    helpdesk_ticket_id = fields.Many2one('helpdesk.ticket', string='Helpdesk Ticket', ondelete='set null')
    sale_order_id = fields.Many2one('sale.order', string='Sales Order')
