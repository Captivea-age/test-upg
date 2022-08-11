# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import models, fields, api, _
from math import radians, cos, sin, asin, sqrt
from odoo.exceptions import UserError, ValidationError
import pytz
from dateutil import tz
import calendar


class ProjectTask(models.Model):
    _inherit = 'project.task'
    
    def wizard_app(self):
        ctx = {
            'default_service_task_id': self.id,
            'default_department_id': self.department_id.id,
            'default_job_type_id': self.job_type_id.id,
            'default_field_technician_id': self.user_id.id,
            'default_date': self.start_date,
        }
        
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'field.service.appointment',
            'view_id': self.env.ref('cap_studio_customization.view_field_service_appointment_form').id,
            'domain': [('id', '!=', self.id)],
            'target': 'new',
            'context': ctx,
        }


class FieldServiceAppointment(models.TransientModel):
    _name = 'field.service.appointment'
    _description = 'Field Service Appointment'

    field_technician_id = fields.Many2one('res.users', string='Field Technician')
    date = fields.Date(string='Day', default=lambda self: fields.Date.context_today(self))
    department_id = fields.Many2one('cap.department', string='Department', ondelete='set null')
    job_type_id = fields.Many2one('job.type', string='Job Type', ondelete='set null')
    service_task_ids = fields.Many2many('project.task', string='Service Task')
    service_task_id = fields.Many2one('project.task', string='Task')

    @api.onchange('date', 'field_technician_id')
    def _onchange_get_task(self):
        if self.date and self.field_technician_id:
            service_tasks = self.env['project.task'].search([('start_date', '=', self.date), ('user_id', '=', self.field_technician_id.id), ('id', '!=', self._context.get('active_id'))])
        if self.date and not self.field_technician_id:
            service_tasks = self.env['project.task'].search([('start_date', '=', self.date), ('id', '!=', self._context.get('active_id'))])
        if service_tasks:
            self.service_task_ids = [(6, 0, service_tasks.ids)]
        else:
            self.service_task_ids = False

    def find_appointment(self):
        already_appointments = self.env['appointment.selection'].search([])
        if already_appointments:
            already_appointments.unlink()
        task = self.env['project.task'].browse(self._context.get('active_id'))
        if self.service_task_ids:
            for user in self.service_task_ids.mapped('user_id'):
                available_appointment_time = []
                appointment_time_taken = []
                time_not_available = []
                time_not_available1 = []

                for service_task_id in self.service_task_ids.filtered(lambda rec: rec.user_id.id == user.id):
                    if service_task_id.planned_hour_start and service_task_id.planned_hour_end:
                        taken_time = self.env['time.selection'].search([('minutes', '>', service_task_id.planned_hour_start.minutes), ('minutes', '<', service_task_id.planned_hour_end.minutes)])
                        time_not_available += taken_time.mapped('minutes')
                        # time_not_available.append(taken_time.mapped('minutes'))
                time_not_available = list(dict.fromkeys(time_not_available))
                time_not_available.sort()
                available_appointment_time = self.env['time.selection'].search([('minutes', 'not in', time_not_available),('minutes', '>=', 480),('minutes', '<=', 1200)]).mapped('minutes')

                job_min = self.job_type_id.time_needed_hours * 60
                job_time_qtr = (job_min / 15)

                jobtype_possible_appointment = []
                for available_appointment in available_appointment_time:
                    possible_time = []
                    a_time = 0
                    if (available_appointment + job_min) in available_appointment_time:
                        a_time = available_appointment
                        for rec in range(0, int(job_time_qtr)+1):
                            if a_time in available_appointment_time:
                                possible_time.append(a_time)
                                a_time+=15
                            else:
                                break
                    if len(possible_time) == (job_time_qtr+1):
                        jobtype_possible_appointment.append(possible_time)
                job_possible_appointments = []
                new_job_possible_appointment = []
                for service_task_id in self.service_task_ids.filtered(lambda rec: rec.user_id.id == user.id).sorted(key=lambda r: r.planned_hour_start.minutes):
                    for possible_time_slot in jobtype_possible_appointment:
                        if service_task_id.planned_hour_start.minutes == possible_time_slot[-1] or service_task_id.planned_hour_end.minutes == possible_time_slot[0]:
                            if possible_time_slot not in job_possible_appointments:
                                flag = 0
                                for possible_time in possible_time_slot:
                                    if possible_time in new_job_possible_appointment:
                                        flag = 1
                                        continue
                                if not flag:
                                    new_job_possible_appointment += possible_time_slot
                                    job_possible_appointments.append(possible_time_slot)

                for service_task_id in self.service_task_ids.filtered(lambda rec: rec.user_id.id == user.id).sorted(key=lambda r: r.planned_hour_start.minutes):
                    cnt = 0
                    for job_possible_appointment in job_possible_appointments:
                        if job_possible_appointment:
                            if service_task_id.planned_hour_start.minutes == job_possible_appointment[-1] or service_task_id.planned_hour_end.minutes == job_possible_appointment[0]:
                                start_time_id = self.env['time.selection'].search([('minutes', '=', job_possible_appointment[0]), ('minutes', '>=', 480)], limit=1)
                                end_time_id = self.env['time.selection'].search([('minutes', '=', job_possible_appointment[-1]), ('minutes', '<=', 1200)], limit=1)
                                appointment_partner = service_task_id.partner_id
                                task_partner = task.partner_id
                                location_distance = self._get_location_distance(appointment_partner.partner_latitude, appointment_partner.partner_longitude, task_partner.partner_latitude, task_partner.partner_longitude)
                                self.env['appointment.selection'].create({
                                    'start_time_id': start_time_id.id,
                                    'end_time_id': end_time_id.id,
                                    'user_id': service_task_id.user_id.id,
                                    'location_distance': location_distance,
                                    'service_task_id': service_task_id.id,
                                    'task_id': task.id,
                                })
                                job_possible_appointments.remove(job_possible_appointment)
                                job_possible_appointments.insert(cnt, [])
                                cnt += 1

                # Extra First job appointment
                start_time_id = self.env['time.selection'].search([('minutes', '=', 480)], limit=1)
                end_time_minutes = start_time_id.minutes + job_min
                end_time_id = self.env['time.selection'].search([('minutes', '=', end_time_minutes)], limit=1)
                warehouse_to_job_times = []
                start_minute = start_time_id.minutes
                for rec in range(0, int(job_time_qtr)):
                    warehouse_to_job_times.append(start_minute)
                    start_minute += 15
                flag = 0
                for time in warehouse_to_job_times:
                    if time in (time_not_available + new_job_possible_appointment):
                        flag = 1
                        break
                if not flag:
                    employee = self.env['hr.employee'].search([('user_id', '=', user.id)])
                    appointment_partner = self.env['res.partner']
                    if employee:
                        if employee.address_id:
                            appointment_partner = employee.address_id
                        else:
                            appointment_partner = employee.company_id.partner_id

                        task_partner = task.partner_id
                        location_distance = self._get_location_distance(appointment_partner.partner_latitude, appointment_partner.partner_longitude, task_partner.partner_latitude, task_partner.partner_longitude)
                        self.env['appointment.selection'].create({
                            'start_time_id': start_time_id.id,
                            'end_time_id': end_time_id.id,
                            'user_id': user.id,
                            'location_distance': location_distance,
                            'service_task_id': False,
                            'task_id': task.id,
                        })
        else:
            all_technician_users = self.env['res.users'].search([('technician_bool', '=', True)])
            job_min = self.job_type_id.time_needed_hours * 60
            job_time_qtr = (job_min / 15)
            start_time_id = self.env['time.selection'].search([('minutes', '=', 480)], limit=1)
            end_time_minutes = start_time_id.minutes + job_min
            end_time_id = self.env['time.selection'].search([('minutes', '=', end_time_minutes)], limit=1)

            for user in all_technician_users:
                employee = self.env['hr.employee'].search([('user_id', '=', user.id)])
                appointment_partner = self.env['res.partner']
                if employee:
                    if employee.address_id:
                        appointment_partner = employee.address_id
                    else:
                        appointment_partner = employee.company_id.partner_id

                    task_partner = task.partner_id
                    location_distance = self._get_location_distance(appointment_partner.partner_latitude, appointment_partner.partner_longitude, task_partner.partner_latitude, task_partner.partner_longitude)
                    self.env['appointment.selection'].create({
                        'start_time_id': start_time_id.id,
                        'end_time_id': end_time_id.id,
                        'user_id': user.id,
                        'location_distance': location_distance,
                        'service_task_id': False,
                        'task_id': task.id,
                    })

        return  {
            'name': _('Appointments'),
            'view_mode': 'form',
            'res_model': 'appointment.selection.wizard',
            'view_id': self.env.ref('cap_studio_customization.view_appointment_selection_wizard_tree').id,
            'type': 'ir.actions.act_window',
            'context': {
                'default_field_technician_id': self.field_technician_id.id, 
                'default_date': self.date,
                'default_date_time': datetime.now(),
            },
            'target': 'new'
        }

    def _get_location_distance(self, lat1, long1, lat2, long2):
        # convert decimal degrees to radians 
        lat1, long1, lat2, long2 = map(radians, [lat1, long1, lat2, long2])
        # haversine formula 
        dlon = long2 - long1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        # Radius of earth in kilometers is 6371
        km = 6371* c
        mile = km * 0.62137
        return mile


class AppointmentSelectionWizard(models.TransientModel):
    _name = 'appointment.selection.wizard'
    _description = 'Appointment Selection Wizard'

    field_technician_id = fields.Many2one('res.users', string='Field Technician')
    date = fields.Date(string='Day')
    appointment_selection_ids = fields.Many2many('appointment.selection', string='Appointments')
    is_appoinment_available = fields.Boolean(string='Appointment Available ?')
    #Added for the go back button
    service_task_id = fields.Many2one('project.task', string='Task')
    department_id = fields.Many2one('cap.department', string='Department', ondelete='set null')
    job_type_id = fields.Many2one('job.type', string='Job Type', ondelete='set null')

    def goBack(self):
        ctx = {
            'default_service_task_id': self.service_task_id.id,
            'default_department_id': self.department_id.id,
            'default_job_type_id': self.job_type_id.id,
            'active_id':self.service_task_id.id,
        }
        
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'field.service.appointment',
            'view_id': self.env.ref('cap_studio_customization.view_field_service_appointment_form').id,
            'domain': [('id', '!=', self.service_task_id.id)],
            'target': 'new',
            'context': ctx,
        }

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        appointments = self.env['appointment.selection'].search([])
        if appointments:
            res['appointment_selection_ids'] = [(6, 0, appointments.ids)]
            res['is_appoinment_available'] = True
        return res

    @api.onchange('date')
    def _onchange_date(self):
        self.appointment_selection_ids.write({'date': self.date})

    @api.onchange('date', 'field_technician_id')
    def _onchange_get_task(self):
        if self.field_technician_id:
            appointment_selection_job = self.appointment_selection_ids.search([('user_id', '=', self.field_technician_id.id)])
        else:
            appointment_selection_job = self.env['appointment.selection'].search([])
        if appointment_selection_job:
            appointment_selection_job.write({'date': self.date})
            self.appointment_selection_ids = [(6, 0, appointment_selection_job.ids)]
        else:
            self.appointment_selection_ids = False


class AppointmentSelection(models.Model):
    _name = 'appointment.selection'
    _description = 'Appointment Selection'
    _order = 'location_distance'

    start_time_id = fields.Many2one('time.selection', string='Start Time')
    end_time_id = fields.Many2one('time.selection', string='End Time')
    location_distance = fields.Float(string='Location Distance (In Miles)')
    service_task_id = fields.Many2one('project.task', string='Service Task')
    date = fields.Date(string='Appointment Date')
    user_id = fields.Many2one('res.users', string='Assign To')
    task_id = fields.Many2one('project.task', string='Task')

    def select_appointment(self):
        start_date = str(self.date) +' '+ self.start_time_id.name
        end_date = str(self.date) +' '+ self.end_time_id.name
        planned_start_date = datetime.strptime(start_date, '%Y-%m-%d %I:%M %p')
        planned_end_date = datetime.strptime(end_date, '%Y-%m-%d %I:%M %p')

        date_begin = planned_start_date
        date_end = planned_end_date

        c = calendar.Calendar(firstweekday=calendar.SUNDAY)
        year = datetime.now().year
        nov_month = 11
        mar_month = 3

        mar_monthcal = c.monthdatescalendar(year,mar_month)
        sec_sunday_of_mar = [day for week in mar_monthcal for day in week if \
                        day.weekday() == calendar.SUNDAY and \
                        day.month == mar_month][1]

        nov_monthcal = c.monthdatescalendar(year,nov_month)
        first_sunday_of_nov = [day for week in nov_monthcal for day in week if \
                        day.weekday() == calendar.SUNDAY and \
                        day.month == nov_month][0]

        est_zone = ''

        if first_sunday_of_nov > self.date > sec_sunday_of_mar:
            est_zone = 'EST5EDT'
        else:
            est_zone = 'EST'

        if est_zone:
            est_timezone = str(datetime.now(pytz.timezone(est_zone))).split('-')[-1]
            est_timezone = est_timezone.split(':')
            hour = int(est_timezone[0])
            minute = int(est_timezone[1])

            date_begin = planned_start_date - timedelta(hours=hour, minutes=minute)
            date_end = planned_end_date - timedelta(hours=hour, minutes=minute)

        self.task_id.update({
            'planned_date_begin': date_begin,
            'planned_date_end': date_end,
            'planned_hour_start': self.start_time_id.id,
            'planned_hour_end': self.end_time_id.id,
            'user_id': self.user_id.id,
            'start_date': self.date,
            'arrival_window': False,
        })

        self.env['appointment.selection'].search([]).unlink()
