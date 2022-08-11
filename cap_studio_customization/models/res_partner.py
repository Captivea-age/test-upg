# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    location_type_1_id = fields.Many2one('contact.location.relationship', string='z- do not use', ondelete='set null')
    historical_job_notes = fields.Html(compute='_compute_historical_job_notes', string='Historical Job Notes')
    sales_list_ids = fields.One2many('sale.order', 'partner_id', string='Sales List')
    job_task_history_ids = fields.One2many('project.task', 'location_id', string='Job Task History')
    invoice_list_ids = fields.One2many('account.move', 'partner_id', string='Invoice List')
    monstercare_list_ids = fields.One2many('sale.subscription', 'partner_id', string='Monstercare List')
    inspection_notifications_ids = fields.One2many('preventive_maintenance.notification', 'location_id', string='Inspection Notifications')
    systems_list_ids = fields.One2many('preventive_maintenance.system', 'location_id', string='Systems List')
    project_task_ids = fields.One2many('project.task', 'location_id', string='Project Tasks')
    job_picture_history_ids = fields.One2many('project.task', 'location_id', string='Job Picture History')
    state_code = fields.Char(related='state_id.code', string='State Code', store=True)
    preferred_contact_method = fields.Selection([('email', 'email'), ('phone call', 'phone call'), ('SMS', 'SMS')], string='Preferred Contact Method')
    customer_type = fields.Selection([('Residential', 'Residential'), ('Commercial', 'Light Commercial'), ('Heavy Commercial', 'Heavy Commercial')], string='Old Location Type')
    st_contact = fields.Char(string='ST Contact ID')
    description = fields.Char(string='Description')
    extra_mobile_numbers = fields.Char(string='Extra Mobile Numbers')
    extra_phone_numbers = fields.Char(string='Extra Phone Numbers')
    state_code_1 = fields.Char(string='State Code')
    st_location = fields.Char(string='ST Location ID')
    extra_email_addresses = fields.Char(string='Extra Email Addresses')

    @api.depends('create_date')
    def _compute_historical_job_notes(self):
        for record in self:
            table =""
            header = "<table class='table table-striped table-hover'><tr><th>Job date</th><th>Type</th><th>Name</th><th>Summary</th><th>Notes</th></tr>"
            body = ""
            footer = "</table>"
            jobs = record.env['project.task'].search([('partner_id','=',record.id),('is_fsm','=',True)])
            if len(jobs)>0:
                for job in jobs:
                    if job['planned_date_begin']:
                        body+="<tr><td>"+str(datetime.datetime.strftime(job['planned_date_begin'],"%d/%m/%Y" ))+"</td><td>"+str(job['job_type_id']['name'])+"</td><td>"+str(job['name'])+"</td><td>"+str(job['description'])+"</td><td><h4>"+str(job['job_notes'])+"<h4></td></tr>"
                    table = str(header)+str(body)+str(footer)

            record['historical_job_notes'] = table
