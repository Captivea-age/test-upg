# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ContactLocationRelationship(models.Model):
    _name='contact.location.relationship'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Contact Location Relationship'
    _order = 'sequence asc, id asc'

    name = fields.Char(string='Name')
    active = fields.Boolean('Active')
    sequence = fields.Integer(string='Sequence')
    contact_id = fields.Many2one('res.partner', string='Contact')
    contact_city = fields.Char('Contact City')
    contact_country = fields.Many2one('res.country', string='Contact Country')
    contact_email = fields.Char(string='Contact Email')
    contact_mobile = fields.Char(string='Contact Mobile')
    contact_phone = fields.Char(string='Contact Phone')
    contact_roles_ids = fields.Many2many('contact.role', string='Contact Roles')
    contact_state_ids = fields.Many2one('res.country.state', string='Contact State')
    contact_street = fields.Char(string='Contact Street')
    contact_street2 = fields.Char(string='Contact Street 2')
    contact_zip = fields.Char(string='Contact Zip')

    location_id = fields.Many2one('res.partner', string='Location')
    new_location_name = fields.Char(string='Location Name')
    new_location_city = fields.Char('location City')
    new_location_country_id = fields.Many2one('res.country', string='Location Country')
    new_location_state_id = fields.Many2one('res.country.state', string='Location State')
    new_location_street = fields.Char(string='Location Street')
    new_location_street_2 = fields.Char(string='Location Street 2')
    new_location_zip = fields.Char(string='Location Zip')
    pick_a_location = fields.Selection([('New Location', 'New Location'),
                                        ('Existing Location', 'Existing Location'),
                                        ('Same Address than the contact', 'Same Address than the contact')],
                                        string='Pick a location')
    preferred_contact_method_ids = fields.Many2many('contact.method', string='Preferred Contact Method')
    relationship_type = fields.Selection([('Resident Owner','Resident owner'),('Tenant','Tenant'),
                                          ('Property Manager','Property manager'),('Landlord','Landlord'),
                                          ('Other Contact','Other Contact')], string='Relationship Type')
