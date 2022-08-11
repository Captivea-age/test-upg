# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    portal_access_ids = fields.Many2many('res.partner', compute='_compute_portal_access', string='Contact')
    invoiced_id = fields.Many2one('res.partner', string='Invoiced', copy=True, ondelete='set null')
    helpdesk_ticket_id = fields.Many2one('helpdesk.ticket', string='Helpdesk Ticket', ondelete='set null')
    in_process = fields.Boolean(string='In Process')
    val_50 = fields.Boolean(string='50%')
    val_25 = fields.Boolean(string='25%')
    val_75 = fields.Boolean(string='75%')
    default_values_done = fields.Boolean(string='Default values done')
    cost_only_invoicing = fields.Boolean(string='Cost Only Invoicing')
    void = fields.Html(string='Void',store=True)
    contact_list_ids = fields.One2many(related='partner_id.contact_list_ids', string='Contact Lists')
    related_job_type = fields.Char(related='task_id.job_type_id.display_name', string='Related Job Type')
    stock_picking_count = fields.Integer(compute='_compute_stock_picking_count', string='Sales Order count')
    purchase_order_count = fields.Integer(compute='_compute_purchase_order_count', string='Purchase Order Count')
    filtered_task_id = fields.Many2one('project.task', string='Filtered Task', ondelete='set null')
    deposit_to_be_paid = fields.Selection([('25%', '25%'), ('50%', '50%'), ('75%', '75%')],string='Deposit to be Paid')

    def _compute_stock_picking_count(self):
        self.stock_picking_count = 0
        results = self.env['stock.picking'].read_group([('sale_id', 'in', self.ids)], ['sale_id'], ['sale_id'])
        dic = {}
        for x in results:
            dic[x['sale_id'][0]] = x['sale_id_count']
            for record in self:
                record['stock_picking_count'] = dic.get(record.id, 0)

    def _compute_purchase_order_count(self):
        self.purchase_order_count = 0
        results = self.env['purchase.order'].read_group([('sale_order_id', 'in', self.ids)], ['sale_order_id'], ['sale_order_id'])
        dic = {}
        for x in results:
            dic[x['sale_order_id'][0]] = x['sale_order_count']
            for record in self:
                record['purchase_order_count'] = dic.get(record.id, 0)

    @api.depends('partner_id')
    def _compute_portal_access(self):
        for record in self:
            record['portal_access_ids'] = []
            contact_ids = []
            
            for contact in record['contact_list_ids']:
              record.write({
                'portal_access_ids': [(4, contact.contact_id.id)]
            })

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    product_type = fields.Selection(related='product_id.type', string='Type')
