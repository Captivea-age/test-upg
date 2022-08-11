# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class JobType(models.Model):
    _name='job.type'
    _description = 'Job Type'
    _order = "name asc"

    name = fields.Char(string='Name')
    active = fields.Boolean(string='Active', default=True)
    department_id = fields.Many2one('cap.department', string='Department', ondelete='set null')
    tags_to_add_ids = fields.Many2many('helpdesk.tag', 'helpdesk_tag_job_type_rel', 'tag_id', 'job_type_id', string='Tags To Add')
    location_types_ids = fields.Many2many('location.type', 'job_type_location_type_rel', 'job_type_id', 'location_type_id', string='Location Types')
    installation_type = fields.Boolean(string='Installation Type')
    time_needed_hours = fields.Float(string='Time needed (hours)')
    description = fields.Text(string='Description')
    sequence = fields.Integer(string='Sequence')
    default_quotation_template = fields.Many2one('sale.order.template', string='Default Quotation Template', ondelete='set null')
    analytic_tag_ids = fields.Many2many('account.analytic.tag',string="Analytic tags")
    
# class JobType(models.Model):
#     _name='job.type'
#     _description = 'Job Type'

#     name = fields.Char(string='Name')
#     active = fields.Boolean(string='Active')
#     default_quotation_template = fields.Many2one('sale.order.template', string='Default Quotation Template')
#     department = fields.Many2one('cap.department', string='Department')
#     description = fields.Text(string='Description')
#     installation_type = fields.Boolean(string='Installation')
#     location_types = fields.Many2many('x_location_type', string='Types')
#     tags_to_add = fields.Many2many('helpdesk.tag', string='Tags')
#     time_needed_hours = fields.Float(string='Time needed (hours)')
