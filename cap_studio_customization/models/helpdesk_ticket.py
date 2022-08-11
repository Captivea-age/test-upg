# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    location_id = fields.Many2one('res.partner', string='Location')
    customer_email = fields.Char(related='pick_the_location_id.contact_id.email',string='Customer Email', readonly=True)
    pick_the_location_id = fields.Many2one('contact.location.relationship', string='Pick the location contact', copy=True, store=True)
    customer_name = fields.Many2one('res.partner', related='pick_the_location_id.contact_id', string='Customer Name', store=True)
    contact_id = fields.Many2one('res.partner', string='Contact', ondelete='set null', copy=True)
    customer_search_id = fields.Many2one('res.partner', string='Customer Search', ondelete='set null', copy=True)
    department_assigned_id = fields.Many2one('hr.department', string='Department Assigned', ondelete='set null')
    employee_assigned_id = fields.Many2one('hr.employee', string='Employee Assigned', ondelete='set null')
    sale_order_count = fields.Integer(compute='_compute_sale_order_count', string='Helpdesk Ticket Count')
    purchase_order_count = fields.Integer(compute='_compute_purchase_order_count', string='Helpdesk Ticket Count')
    job_type_id = fields.Many2one('job.type', string='Job Type', ondelete='set null')
    modify_location_contact = fields.Boolean(string='Modify Location Contact')
    time_needed = fields.Float(string='Time needed')
    job_notes_recap_table = fields.Html(compute='_compute_job_notes_recap_table')
    systems_to_be_inspected = fields.Html(string='Systems to be Inspected')
    to_remove = fields.Text(string='To Remove')
    job_notes_recap = fields.Text(string='Job Notes Recap')
    jobs_list_ids = fields.One2many('project.task', 'helpdesk_ticket_id', string='Job Lists')
    jobs_list_1_ids = fields.One2many('project.task', 'helpdesk_ticket_id', string='Jobs Lists')
    email = fields.Char(related='partner_id.email', string='Email', store=True)
    location_street2 = fields.Char(related='partner_id.street2', string='Location Street2', store=True)
    location_state = fields.Many2one('res.country.state', related='partner_id.state_id', string='Location State', store=True)
    phone_2 = fields.Char(related='pick_the_location_id.contact_id.phone', string='Mobile', store=True)
    state_code = fields.Char(related='partner_id.state_code', string='State Code', store=True)
    monstercare_list_ids = fields.One2many('sale.subscription', 'partner_id', related='contact_id.monstercare_list_ids', string='Monstercare List', store=True)
    customer_phone = fields.Char(related='partner_id.phone', string='Customer Phone', store=True)
    monstercare_list_1 = fields.One2many('sale.subscription','partner_id', related='location_id.monstercare_list_ids', string='Monstercare lists', store=True)
    monstercare_subscriptions = fields.Integer(related='location_id.subscription_count', string='MonsterCare Subscriptions')
    contact_name = fields.Many2one('res.partner', related='pick_the_location_id.contact_id', string='Contact Name', store=True)
    location_street = fields.Char(related='partner_id.street', string='Location Street', store=True)
    phone = fields.Char(related='location_id.phone', string='Landline', store=True)
    location_type_1 = fields.Char(related='partner_id.location_type_id.name', string='Location Type', store=True)
    street = fields.Char(related='pick_the_location_id.contact_id.street', string='Street', store=True)
    preferred_contact_method_ids = fields.Many2many('contact.method', 'helpdesk_ticket_contact_method_rel_1', 'ticket_id', 'method_id', related='pick_the_location_id.preferred_contact_method_ids' ,string='Contact Methods')
    #customer_email_1 = fields.Char(related='partner_id.email', string='Customer Email', store=True)
    contact_list_ids = fields.One2many(related='partner_id.contact_list_ids', string='Contact Lists')
    phone_number = fields.Char(related='partner_id.phone', string='Phone Number', store=True)
    #Duplicate of customer email, to be removed and replaced in the form view
    email_2 = fields.Char(related='pick_the_location_id.contact_id.email', string='Email', store=True)
    location_city = fields.Char(related='partner_id.city', string='Location City', store=True)
    location_type = fields.Many2one('location.type', related='location_id.location_type_id', string='Location Type', store=True)
    sales_order_items = fields.One2many(related='sale_order_id.order_line', string='Sales Order Items')
    phone_numbers_ids = fields.One2many(related='customer_name.phone_number_ids', string='Phone Numbers')
    systems_list_ids = fields.One2many(related='partner_id.systems_list_ids')
    location_child_ids = fields.One2many(related='location_id.child_ids', string='Location Childs')
    mobile_phone = fields.Char(related='partner_id.mobile', string='Mobile Phone', store=True)
    systems_to_be_inspected_1 = fields.One2many(related='location_id.inspection_notifications_ids', string='Systems to be inspected')
    customer_phone_1 = fields.Char(related='location_id.phone', string='Customer Phone', store=True)
    location_zip = fields.Char(related='partner_id.zip', string='Location Zip', store=True)
    create_from_the_task_id = fields.Many2one('project.task', string='Create From the task', ondelete='set null')
    products_purchased_ids = fields.Many2many('purchase.order.line', string='Products purchased', compute='_compute_products_purchased')
    remove_this_field = fields.Char(string='remove this field')
    extra_phone = fields.Char(string='Extra Phone')
    extra_phone_name = fields.Char(string='Extra Phone Name')
    preferred_contact_method_1 = fields.Many2many('contact.method', 'helpdesk_ticket_contact_method_rel', 'helpdesk_ticket_id', 'method_id', related='pick_the_location_id.preferred_contact_method_ids',string='Preferred Contact Method')
    related_invoices_ids = fields.Many2many('account.move', compute='_compute_related_invoice', string='Ticket Invoice(s)')
    related_repairs_invoices_ids = fields.Many2many('account.move', compute='_compute_related_repairs_invoices', string='Related Repairs Invoice(s)')
    related_sales_invoices_ids = fields.Many2many('account.move', compute='_compute_related_sales_invoices', string='Related Sales Invoice(s)')
    purchase_order_ids = fields.One2many('purchase.order','helpdesk_ticket_id',string='Purchase Orders')

    @api.depends('sale_order_id')
    def _compute_related_sales_invoices(self):
        self.related_sales_invoices_ids = []
        for record in self:
            invoices = []
  
            if record['sale_order_id']:
                invoices = record['sale_order_id']['invoice_ids']
  
            record['related_sales_invoices_ids'] = invoices

    @api.depends('repair_ids')
    def _compute_related_repairs_invoices(self):
        self.related_repairs_invoices_ids = []
        for record in self:
            invoices = []
            if record['repair_ids']:
                invoices = record['repair_ids'].mapped('invoice_id')

            record['related_repairs_invoices_ids'] = invoices

    @api.depends('fsm_task_ids')
    def _compute_related_invoice(self):
        self.related_invoices_ids = []
        for record in self:
            invoices = []
            if record['fsm_task_ids']:
                sales_orders = record['fsm_task_ids'].mapped('sale_order_id')
                if sales_orders:
                    right_so = sales_orders.filtered(lambda so: so.cost_only_invoicing == False)[0]
                
                    if right_so:
                        invoices = right_so['invoice_ids']
                
                record['related_invoices_ids'] = invoices


    @api.depends('__last_update')
    def _compute_products_purchased(self):
        for record in self:
            lines = False
            pos = self.env['purchase.order'].search([('helpdesk_ticket_id','=',record.id)])
            if len(pos) > 0:
                pol = self.env['purchase.order.line'].search([('order_id','in',pos.ids)])
                lines = pol.ids
            record['products_purchased_ids'] = lines

    @api.depends('__last_update', 'fsm_task_count')
    def _compute_job_notes_recap_table(self):
        for record in self:
            table =""
            header = "<table class='table table-striped table-hover'><tr><th>Job date</th><th>Type</th><th>Name</th><th>Notes</th></tr>"
            body = ""
            footer = "</table>"
            jobs = record.env['project.task'].search([('helpdesk_ticket_id','=',record['id'])])
            if len(jobs)>0:
                for job in jobs:
                    body+="<tr><td>"+str(job['planned_date_begin'])+"</td><td>"+str(job['job_type_id']['name'])+"</td><td>"+str(job['name'])+"</td><td><h4>"+str(job['job_notes'])+"<h4></td></tr>"
                table = str(header)+str(body)+str(footer)
            record['job_notes_recap_table'] = table

    def _compute_purchase_order_count(self):
        self.purchase_order_count = 0
        results = self.env['purchase.order'].read_group([('helpdesk_ticket_id', 'in', self.ids)], ['helpdesk_ticket_id'], ['helpdesk_ticket_id'])
        dic = {}
        for x in results:
            dic[x['helpdesk_ticket_id'][0]] = x['helpdesk_ticket_id_count']
            for record in self:
                record['purchase_order_count'] = dic.get(record.id, 0)

    def _compute_sale_order_count(self):
        self.sale_order_count = 0
        results = self.env['sale.order'].read_group([('helpdesk_ticket_id', 'in', self.ids)], ['helpdesk_ticket_id'], ['helpdesk_ticket_id'])
        dic = {}
        for x in results:
            dic[x['helpdesk_ticket_id'][0]] = x['helpdesk_ticket_id_count']
            for record in self:
                record['sale_order_count'] = dic.get(record.id, 0)
