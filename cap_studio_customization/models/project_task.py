# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import date, datetime
import calendar
import pytz

class ProjectTask(models.Model):
    _inherit = 'project.task'

    street = fields.Char(related='pick_the_location_id.contact_id.street', string='Street', store=True)
    customer_search_id = fields.Many2one('res.partner', string='Customer Search', ondelete='set null', copy=True)
    hr_department_id = fields.Many2many('hr.department', 'hr_department_project_task_rel', 'hr_department_id', 'project_task_id', string='Department')
    department_id = fields.Many2one('cap.department', string='Department', ondelete='set null')
    sale_order_count = fields.Integer(compute='_compute_sale_order_count', string='Filtered Task Count')
    helpdesk_ticket_ids = fields.Many2many('helpdesk.ticket', 'helpdesk_ticket_project_task_rel', 'ticket_id', 'task_id', string='No')
    historical_notes_ids = fields.Many2many('historical.notes', 'project_task_historical_notes_rel', 'task_id', 'notes_ids', string='Historical Notes')
    historical_pictures_ids = fields.Many2many('historical.pictures', 'project_task_historical_pictures_rel', 'task_id', 'picture_id', string='Historical Pictures')
    job_type_id = fields.Many2one('job.type', string='Job Type', ondelete='set null')
    arrived_at_location = fields.Boolean(string='Arrived at Location')
    points_distributed = fields.Boolean(string='Points Distributed')
    out_of_hours_intervention = fields.Boolean(string='Out of Hours Intervention')
    job_confirmed = fields.Boolean(string='Job Confirmed')
    job_finished = fields.Boolean(string='Job finished')
    who_needs_to_follow_up = fields.Boolean(string='Who Needs to follow up?')
    emergency = fields.Boolean(string='Emergency')
    start_date = fields.Date(string='Start Date')
    end_job = fields.Datetime(string='End Job')
    start_job = fields.Datetime(string='Start Job')
    start_drive = fields.Datetime(string='Start Drive')
    end_drive = fields.Datetime(string='End Drive')
    sold_price = fields.Float(compute='_compute_sold_price', string='Sold Price')
    tests_to_perform_html = fields.Html(compute='_compute_tests_to_perform_html', string='Tests to Perform')
    new_html = fields.Html(string='New Html')
    location_city = fields.Char(related='pick_the_location_id.location_id.street', string='Location City')
    location_street = fields.Char(related='pick_the_location_id.location_id.street', string='Location Street', store=True)
    location_zip = fields.Char(related='pick_the_location_id.location_id.zip', string='Location Zip', store=True)
    deep_link = fields.Html(compute='_compute_deep_link', string='Deep Link')
    new_deep_link = fields.Html(string='New Deep Link', store=True)
    pic_6 = fields.Binary(string='Pic 6')
    pic_4 = fields.Binary(string='Pic 4')
    pic_3 = fields.Binary(string='Pic 3')
    pic_2 = fields.Binary(string='Pic 2')
    pic_5 = fields.Binary(string='Pic 5')
    pic_1 = fields.Binary(string='Pic 1')
    reason_for_no_payment = fields.Text(string='Reason for no Payment')
    no_tracking_reason = fields.Text(string='No Tracking Reason')
    new_multiline_text = fields.Text(string='New Multiline Text')
    reason_for_not_invoicing = fields.Text(string='Reason for not Invoicing')
    job_notes = fields.Text(string='Job Notes')
    sale_orders_ids = fields.One2many('sale.order', 'task_id', string='Sale Orders')
    invoice_payment_status = fields.Selection(related='sale_order_id.invoice_ids.payment_state', store=True)
    project_name = fields.Char(related='project_id.display_name', string='Project', store=True)
    extra_phone = fields.Char(related='helpdesk_ticket_id.extra_phone', string='Extra Phone', store=True)
    customer_address = fields.Char(related='pick_the_location_id.contact_street', string='Customer Address', store=True)
    preferred_contact_method = fields.Selection(related='partner_id.preferred_contact_method', string='Preferred Contact Method', store=True)
    location_type_related = fields.Char(related='pick_the_location_id.location_id.location_type_id.display_name', string='Location Type')
    phone_number_1 = fields.Char(related='partner_id.phone', string='Phone Number', store=True)
    monstercare_list_ids = fields.One2many(related='location_id.monstercare_list_ids', string='Monstercare Lists')
    invoices_list_ids = fields.One2many(related='partner_id.invoice_list_ids', string='Invoice Lists')
    tests_to_perform = fields.One2many(related='helpdesk_ticket_id.notification_ids.inspection_ids.tests_done', string='Tests to Perform')
    preferred_contact_method_1 = fields.Many2many('contact.method', 'project_task_contact_method_rel', 'task_id', 'method_id', related='pick_the_location_id.preferred_contact_method_ids',string='Preferred Contact Method')
    state_1 = fields.Char(related='location_id.state_id.name', string='State', store=True, help='Administrative divisions of a country. E.g. Fed. State, Departement, Canton')
    mobile = fields.Char(related='partner_id.mobile', string='Mobile', store=True)
    customers_phone = fields.Char(related='customer_name.phone', string='Customer Phone', store=True)
    location_state = fields.Char(related='pick_the_location_id.location_id.state_id.name', string='Location State', store=True)
    contact_address = fields.Char(related='partner_id.contact_address', string='Customer Address', store=True)
    extra_phone_name = fields.Char(related='helpdesk_ticket_id.extra_phone_name', string='Location Phone', store=True)
    #is_fsm = fields.Boolean(related='project_id.is_fsm', string='Is Fsm', store=True)
    address = fields.Char(related='partner_id.contact_address', string='Address')
    monstercare_list_good_ids = fields.One2many(related='partner_id.monstercare_list_ids', string='Monstercare Lists')
    location_contacts_ids = fields.One2many(related='location_id.contact_list_ids', string='Location Contact')
    allow_truck_assignment = fields.Boolean(related='job_type_id.installation_type', string='Allow truck assignment', store=True)
    invoices = fields.Many2many(relation='account_move_project_task_rel', related='sale_order_id.invoice_ids')
    location_name = fields.Char(related='pick_the_location_id.location_id.display_name', string='Location Name', store='True')
    sales_list_ids = fields.One2many(related='partner_id.sales_list_ids', string='Sales List')
    location_type_id = fields.Many2one('location.type', related='location_id.location_type_id', string='Location Type')
    address_2 = fields.Char(related='partner_id.contact_address', string='Address')
    subscription_count = fields.Integer(related='partner_id.subscription_count')
    customers_mobile = fields.Char(related='customer_name.mobile', string='Customer Mobile', store=True)
    location_type_1 = fields.Char(related='pick_the_location_id.location_type_id.name', string='Location Type', store=True)
    systems_list_ids = fields.One2many('preventive_maintenance.system', 'location_id', related='partner_id.systems_list_ids', string='System Lists')
    job_picture_history_ids = fields.One2many(related='location_id.job_picture_history_ids')
    job_duration = fields.Char(string='Job Duration')
    test_job_notes = fields.Char(string='Test Job Notes')
    address_1 = fields.Char(string='Address')
    link = fields.Char(compute='_compute_link', string='FormsOnFire:')
    phone_number = fields.Char(string='Phone Number')
    job_duration_display = fields.Char(string='Length', compute='_compute_job_duration_display')
    out_of_hours_intervention_text = fields.Char(string='Out of hours intervention')
    service_titan_quote = fields.Char(string='Service Titan quote')
    state = fields.Char(string='State')
    technician_team_ids = fields.Many2many('res.users', 'x_task_users_rel', 'project_task_id', 'res_user_id', string='Technician Team')
    truck_assigned = fields.Many2one('project.task', string='Truck Assigned', ondelete='set null')
    # sales_order_id = fields.Many2one('sale.order', string='Sale Order', ondelete='set null')
    job_type = fields.Selection([('AOR: Inspection Fail Recall', 'AOR: Inspection Fail Recall'), ('AOR: Install 0.5 Day', 'AOR: Install 0.5 Day'), ('AOR: Install 1 Day', 'AOR: Install 1 Day'), ('AOR: Install 1.5 Days', 'AOR: Install 1.5 Days'), ('AOR: Install 2 Days', 'AOR: Install 2 Days'), ('AOR: Other Work', 'AOR: Other Work'), ('AOR: Patchwork', 'AOR: Patchwork'), ('AOR: Pre-inspection', 'AOR: Pre-inspection'), ('Com - SCV1', 'Com - SCV1'), ('LOG: AOR Part Pickup - Parts House', 'LOG: AOR Part Pickup - Parts House'), ('LOG: AOR Part Pickup - Transfer Center', 'LOG: AOR Part Pickup - Transfer Center'), ('LOG: SCV2 Part Pickup - Parts House', 'LOG: SCV2 Part Pickup - Parts House'), ('LOG: SVC2 Part Pickup - Transfer Center', 'LOG: SVC2 Part Pickup - Transfer Center'), ('PM: 1 Sys Maintenance Contract / MonsterCare', 'PM: 1 Sys Maintenance Contract / MonsterCare'), ('PM: 2 Sys Maintenance Contract / MonsterCare', 'PM: 2 Sys Maintenance Contract / MonsterCare'), ('PM: 3 Sys Maintenance Contract / MonsterCare', 'PM: 3 Sys Maintenance Contract / MonsterCare'), ('PM: 4 Sys Maintenance Contract / MonsterCare', 'PM: 4 Sys Maintenance Contract / MonsterCare'), ('PM: 5+ Sys Maintenance Contract / MonsterCare', 'PM: 5+ Sys Maintenance Contract / MonsterCare'), ('PM: Commercial Contract PM', 'PM: Commercial Contract PM'), ('PM: Maintenance Contract / MonsterCare Visit', 'PM: Maintenance Contract / MonsterCare Visit'), ('PM: Promo Quick Check', 'PM: Promo Quick Check'), ('PM: Promotional TuneUp', 'PM: Promotional TuneUp'), ('PM: System Inspection and Report', 'PM: System Inspection and Report'), ('SLS: Estimate Follow up', 'SLS: Estimate Follow up'), ('SLS: Provide Comm Quote', 'SLS: Provide Comm Quote'), ('SLS: Provide Res Quote', 'SLS: Provide Res Quote'), ('SVC1: - Diagnostic', 'SVC1: - Diagnostic'), ('SVC2: Repair, Replace, Upgrade Parts', 'SVC2: Repair, Replace, Upgrade Parts'), ('SVC2: Warranty: Repair, Replace, Upgrade', 'SVC2: Warranty: Repair, Replace, Upgrade'), ('SVC3 - AOR Recall', 'SVC3 - AOR Recall'), ('SVC3 - Recall', 'SVC3 - Recall'), ('SVC3: Comm Recall', 'SVC3: Comm Recall'), ('SVC3: Follow-up Tech Phone Call', 'SVC3: Follow-up Tech Phone Call'), ('SVC3: Labor Warranty Work', 'SVC3: Labor Warranty Work'), ('Warehouse: Please see details below', 'Warehouse: Please see details below')],string='Job Type old field tbr')
    repairs_dept = fields.Selection([('Repair Needed', 'Repair Needed'), ('IAQ Questions', 'IAQ Questions')],string='Repairs Dept')
    ccr_team = fields.Selection([('Schedule Future PM visit', 'Schedule Future PM visit'), ('Other (provide details)', 'Other (provide details)')],string='CCR Team')
    did_you_invoice = fields.Selection([('Yes', 'Yes'), ('No, the office needs to invoice this one', 'No, the office needs to invoice this one'), ('No, I need help to learn how', 'No, I need help to learn how'), ('No, other reason', 'No, other reason')],string='Did you invoice?')
    does_this_customer_require_a_follow_up_1 = fields.Selection([('Yes', 'Yes'), ('No', 'No')],string='Does this customer require a follow up?')
    follow_up_department = fields.Selection([('AOR department', 'AOR department'), ('CCR Manager', 'CCR Manager'), ('CCR Team', 'CCR Team'), ('Repairs Department', 'Repairs Department')],string='Follow Up Department')
    does_this_customer_require_a_follow_up = fields.Selection([('Yes', 'Yes'), ('No', 'No')],string='Does this customer require a follow up?')
    did_you_properly_track_your_materials = fields.Selection([('Yes', 'Yes'), ('No, I need to learn how', 'No, I need to learn how'), ('No, other reason', 'No, other reason')],string='Did you properly track your materials?')
    did_you_get_payment = fields.Selection([('Yes', 'Yes'), ('No, the customer was not available', 'No, the customer was not available'), ('No, other reason', 'No, other reason')],string='Did you get payment?')
    job_task_history_ids = fields.One2many(related='location_id.job_task_history_ids')
    projecttest_id = fields.Many2one('project.project', string='Projecttest', ondelete='set null', store=True)
    location_ids = fields.One2many('project.task', 'location_id')
    parent_location_id = fields.Many2one('res.partner', related='parent_id.location_id', store=True)
    out_of_hours_arrival = fields.Boolean(string='Out of hours arrival')
    zone = fields.Many2one(related='partner_id.zone', string='Zone')
    historical_job_notes_list = fields.Html(compute='_compute_historical_job_notes_list', string='Historical Job Notes List', readonly=True)
    appoinment_selection_ids = fields.One2many('appointment.selection', 'service_task_id', string='Appointment Selection')
    customer_email = fields.Char(related='customer_name.email',string='Customer Email', readonly=True)
    days_until_job = fields.Integer('Days until Job')
    scheduling_integer = fields.Integer(string='z - Scheduling iterations', default=0)


    def _get_march_day(self):
        c = calendar.Calendar(firstweekday=calendar.SUNDAY)
        year = datetime.now().year
        mar_month = 3

        mar_monthcal = c.monthdatescalendar(year,mar_month)
        sec_sunday_of_mar = [day for week in mar_monthcal for day in week if \
                      day.weekday() == calendar.SUNDAY and \
                      day.month == mar_month][1]
        return sec_sunday_of_mar


    def _get_november_day(self):
        c = calendar.Calendar(firstweekday=calendar.SUNDAY)
        year = datetime.now().year
        nov_month = 11

        nov_monthcal = c.monthdatescalendar(year,nov_month)
        first_sunday_of_nov = [day for week in nov_monthcal for day in week if \
                      day.weekday() == calendar.SUNDAY and \
                      day.month == nov_month][0]

        return first_sunday_of_nov

    def _get_est_timezone(self, est_zone):
        return str(datetime.now(pytz.timezone(est_zone))).split('-')[-1]

    @api.depends('partner_id')
    def _compute_historical_job_notes_list(self):
        for record in self:
            table =""
            header = "<table class='table table-striped table-hover'><tr><th>Job date</th><th>Type</th><th>Name</th><th>Summary</th><th>Notes</th></tr>"
            body = ""
            footer = "</table>"
            if record.partner_id.id and record.id:
                jobs = record.env['project.task'].search([('partner_id','=',record.partner_id.id),('is_fsm','=',True),('id','!=',record.id)])

                if len(jobs)>0:
                    for job in jobs:
                        if job.planned_date_begin:
                            body+="<tr><td>"+str(datetime.strftime(job.planned_date_begin,"%m/%d/%Y" ))+"</td><td>"+str(job.job_type_id.name)+"</td><td>"+str(job.name)+"</td><td>"+str(job['description'])+"</td><td><h4>"+str(job.job_notes)+"<h4></td></tr>"
                            table = str(header)+str(body)+str(footer)

            record['historical_job_notes_list'] = table

    @api.depends('create_date','__last_update')
    def _compute_link(self):
        for record in self:
            try:
                STCustname = record['partner_id']['name']
                CSTJobID = str(record['id'])
                CSTCustaddress1 = str(record['location_street'])
                CSTcustcity = record['location_city']
                CSTcustzip = str(record['location_zip'])
                CSTcustemail = str(record['partner_id']['email'])
                CqwSTJobID = str(record['id'])
                
                raw_link = "formsonfire://PMappform?STCustname:"+STCustname+"%7CSTJobID:"+CSTJobID+"%7CSTCustaddress1:"+CSTCustaddress1+"%7CSTcustcity:"+CSTcustcity+"%7CSTcustzip:"+CSTcustzip+"%7CSTcustemail:"+CSTcustemail+"%7CqwSTJobID:"+CqwSTJobID
                clean_link = raw_link.replace(" ","%20")
                final = clean_link
            except:
                final=''
          
            record['link'] = final

    @api.depends('planned_hour_start', 'planned_hour_end')
    def _compute_job_duration_display(self):
        for record in self:
            record['job_duration_display'] = 'The job is scheduled for '
            if record.planned_hour_start != False and record.planned_hour_end != False:
                minutes_float = record.planned_hour_end.minutes - record.planned_hour_start.minutes
                if minutes_float < 0:
                    record['job_duration_display'] = 'You cannot select an end hour before start hour'
                    record['planned_hour_end'] = record.planned_hour_start
                else:
                    hours = int(minutes_float / 60)
                    minutes_left = str(int((minutes_float - (hours * 60)) / 60 * 100))
                    if minutes_left == '0':
                        minutes_left = ""
                    else:
                        minutes_left = "."+minutes_left
#             record['job_duration_display'] = record['job_duration_display']+str(hours)+minutes_left+' hour(s)'
                    record['job_duration_display'] = str(hours)+minutes_left+' hour(s)'

    @api.depends('partner_id', 'location_city','location_street','location_zip')
    def _compute_deep_link(self):
        for record in self:
            try:
                STCustname = record['partner_id']['name']
                CSTJobID = str(record['id'])
                CSTCustaddress1 = str(record['location_street'])
                CSTcustcity = record['location_city']
                CSTcustzip = str(record['location_zip'])
                CSTcustemail = str(record['partner_id']['email'])
                CqwSTJobID = str(record['id'])
                
                raw_link = "formsonfire://PMappform?STCustname:"+STCustname+"%7CSTJobID:"+CSTJobID+"%7CSTCustaddress1:"+CSTCustaddress1+"%7CSTcustcity:"+CSTcustcity+"%7CSTcustzip:"+CSTcustzip+"%7CSTcustemail:"+CSTcustemail+"%7CqwSTJobID:"+CqwSTJobID
                clean_link = raw_link.replace(" ","%XXX")
                clean_link = raw_link.replace("XXX","20")
                final="<a href="+clean_link+">FormsOnFire link :"+clean_link+" </a>"
            except:
                final=''
            record['deep_link'] = final

    @api.depends('helpdesk_ticket_id')
    def _compute_tests_to_perform_html(self):
        for record in self:
            table = []
            helpdesk = self.helpdesk_ticket_id
            tests =  []
            inspections = []

            for notification in helpdesk.notification_ids:
                inspections.append(notification.inspection_ids)
            for inspection in inspections:
                tests.append(inspection.tests_done)

            header = "<table><th>System</th><th>Component</th><th>Test category</th><th>Test</th><th>Test status</th><th>Value</th>"
            body = ""
            footer = "</table>"

            for test_per_system in tests:
                for test in test_per_system:
                    body += "<tr>"
                    body += "<td>"+str(test.system_id.name)+"</td> "
                    body += "<td>"+str(test.component_id.name)+"</td> "
                    body += "<td>"+str(test.test_type.test_type_id.name)+"</td> "
                    body += "<td>"+str(test.test_type.name)+"</td> "
                    body += "<td>"+str(test.result)+"</td> "
                    body += "<td>"+str(test.value)+"</td> "

                    body +="</tr>"
                    test['job_id'] = self.id
            table = header+body+footer

            record['tests_to_perform_html'] = table

    @api.depends('__last_update')
    def _compute_sold_price(self):
        for record in self:
            record['sold_price'] = record["material_line_total_price"]

    def _compute_sale_order_count(self):
        self.sale_order_count = 0
        # TBD To be fixed
        # results = self.env['sale.order'].read_group([('task_id', 'in', self.ids)], ['task_id'], ['task_id'])
        # dic = {}
        # for x in results:
        #     dic[x['task_id'][0]] = x['task_count']
        #     for record in self: 
        #         record['sale_order_count'] = dic.get(record.id, 0)    
