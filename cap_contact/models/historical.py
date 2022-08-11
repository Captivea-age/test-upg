# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class HistoricalNotes(models.Model):
    _name='historical.notes'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Historical Notes'

    name = fields.Char(string='Name', default='Notes')
    active = fields.Boolean(string='Active', default=True, copy=True, tracking=True)
    location_id = fields.Many2one('res.partner', string='Location', ondelete='set null', copy=True)
    job_notes = fields.Text(string='Job Notes')
    reason_for_no_payment = fields.Text(string='Reason for no payment')
    reason_for_not_invoicing = fields.Text(string='Reason for not Invoicing')
    reason_for_not_tracking_materials = fields.Text(string='Reason for not tracking materials')
    origin = fields.Many2one('project.task', string='Origin')
    sequence = fields.Integer(string='Sequence')
    did_you_invoice = fields.Selection([('Yes', 'Yes'), ('No, the office needs to invoice this one', 'No, the office needs to invoice this one'), ('No, I need help to learn how', 'No, I need help to learn how'), ('No, other reason', 'No, other reason')],string='Did you invoice?')
    did_you_get_payment = fields.Selection([('Yes', 'Yes'), ('No, the customer was not available', 'No, the customer was not available'), ('No, other reason', 'No, other reason')],string='Did you get payment?')
    did_you_properly_track_your_materials = fields.Selection([('yes', 'yes'), ('No, I need to learn how', 'No, I need to learn how'), ('No, other reason', 'No, other reason')] ,string='Did you properly track your materials?')


class HistoricalPictures(models.Model):
    _name='historical.pictures'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Historical Pictures'

    name = fields.Char(string='Name', default='Picture')
    active = fields.Boolean(string='Active', copy=True, tracking=True, default=True)
    location_id = fields.Many2one('res.partner', string='Location', ondelete='set null', copy=True)
    job_picture_1 = fields.Binary(string='Job Picture 1', store=True)
    job_picture_2 = fields.Binary(string='Job Picture 2', store=True)
    job_picture_3 = fields.Binary(string='Job Picture 3', store=True)
    job_picture_4 = fields.Binary(string='Job Picture 4', store=True)
    job_picture_5 = fields.Binary(string='Job Picture 5', store=True)
    job_picture_6 = fields.Binary(string='Job Picture 6', store=True)
    origin = fields.Many2one('project.task', string='Origin')
    sequence = fields.Integer(string='Sequence')
