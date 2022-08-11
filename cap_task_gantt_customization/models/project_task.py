# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta


class ProjectTask(models.Model):
    _inherit = 'project.task'

    arrival_window_start = fields.Many2one(related='arrival_window.start_time', string='Start Time')
    arrival_window_end = fields.Many2one(related='arrival_window.end_time', string='End Time')
    compute_color = fields.Integer(string='Comput Color', compute='_get_compute_color')
    task_color = fields.Integer(string='Task Color')
    image_on_tag = fields.Many2many('helpdesk.tag', 'project_tags_image_rel', 'project_tag_id', 'project_tags_image_id',
                                    string='Image on Tags', compute='_get_tags', store=True)
    description_text = fields.Text(string='Description Text')

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        results = super(ProjectTask, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy)
        update_result = []
        for result in results:
            if 'user_id' in result and result['user_id']:
                user = self.user_id.browse(result['user_id'][0])
                if user.technician_bool:
                   update_result.append(result)
                results = update_result
        return results

    @api.onchange('description')
    def _onchange_description(self):
        self.description_text = str(self.description)
        self.description_text = self.description_text.replace('<p>', '').replace('</p>', '').replace('<br>', '\n')

    @api.depends('helpdesk_tag_ids', 'helpdesk_tag_ids.priority')
    def _get_tags(self):
        for rec in self:
            selected_helpdesk_tag_ids = rec.helpdesk_tag_ids.filtered(lambda x: x.priority)
            if selected_helpdesk_tag_ids:
                self.write({'image_on_tag': [(6, 0, selected_helpdesk_tag_ids.ids)]})
            else:
                self.image_on_tag = False

    @api.depends('partner_id')
    def _get_compute_color(self):
        for record in self:
            partner = self.env['res.partner'].search([('id', '=', record.partner_id.id)])
            if partner:
                record.compute_color = partner.zone.color
                record.task_color = record.compute_color
            else:
                record.compute_color = False
                record.task_color = False
                # record.task_color = record.compute_color

    @api.model
    def gantt_unavailability(self, start_date, end_date, scale, group_bys=None, rows=None):
        start_datetime = fields.Datetime.from_string(start_date)
        end_datetime = fields.Datetime.from_string(end_date)
        user_ids = set()

        # function to "mark" top level rows concerning users
        # the propagation of that user_id to subrows is taken care of in the traverse function below
        def tag_user_rows(rows):
            for row in rows:
                group_bys = row.get('groupedBy')
                res_id = row.get('resId')
                if group_bys:
                    # if user_id is the first grouping attribute
                    if group_bys[0] == 'user_id' and res_id:
                        user_id = res_id
                        user_ids.add(user_id)
                        row['user_id'] = user_id
                    # else we recursively traverse the rows
                    elif 'user_id' in group_bys:
                        tag_user_rows(row.get('rows'))

        tag_user_rows(rows)
        resources = self.env['res.users'].browse(user_ids).mapped('resource_ids').filtered(
            lambda r: r.company_id.id == self.env.company.id)
        # we reverse sort the resources by date to keep the first one created in the dictionary
        # to anticipate the case of a resource added later for the same employee and company
        user_resource_mapping = {resource.user_id.id: resource.id for resource in resources.sorted('create_date', True)}
        leaves_mapping = resources._get_unavailable_intervals(start_datetime, end_datetime)

        # function to recursively replace subrows with the ones returned by func
        def traverse(func, row):
            new_row = dict(row)
            if new_row.get('user_id'):
                for sub_row in new_row.get('rows'):
                    sub_row['user_id'] = new_row['user_id']
            new_row['rows'] = [traverse(func, row) for row in new_row.get('rows')]
            return func(new_row)

        cell_dt = timedelta(hours=1) if scale in ['day', 'week'] else timedelta(hours=12)

        # for a single row, inject unavailability data
        project_task = self.env['project.task']

        def inject_unavailability(row):
            new_row = dict(row)
            user_id = row.get('user_id')
            for rec in new_row.get('records'):
                rec['start_drive'] = project_task.browse(rec.get('id')).start_drive
                rec['end_drive'] = project_task.browse(rec.get('id')).end_drive
                rec['start_job'] = project_task.browse(rec.get('id')).start_job
                rec['end_job'] = project_task.browse(rec.get('id')).end_job
            if user_id:
                resource_id = user_resource_mapping.get(user_id)
                if resource_id:
                    # remove intervals smaller than a cell, as they will cause half a cell to turn grey
                    # ie: when looking at a week, a employee start everyday at 8, so there is a unavailability
                    # like: 2019-05-22 20:00 -> 2019-05-23 08:00 which will make the first half of the 23's cell grey
                    notable_intervals = filter(lambda interval: interval[1] - interval[0] >= cell_dt,
                                               leaves_mapping[resource_id])
                    new_row['unavailabilities'] = [{'start': interval[0], 'stop': interval[1]} for interval in
                                                   notable_intervals]
            return new_row

        return [traverse(inject_unavailability, row) for row in rows]
