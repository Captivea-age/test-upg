# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class ContactMethod(models.Model):
    _name='contact.method'
    _description = 'Contact Method'

    name = fields.Char(string='Name')
    active = fields.Boolean(string='Active', default=True)
    sequence = fields.Integer(string='Sequence')


class ContactRole(models.Model):
    _name='contact.role'
    _description = 'Contact Role'

    name = fields.Char(string='Name')
    active = fields.Boolean(string='Active', default=True)
    sequence = fields.Integer(string='Sequence')


class LocationType(models.Model):
    _name='location.type'
    _description = 'Location Type'

    name = fields.Char(string='Name')
    active = fields.Boolean(string='Active', default=True)
    sequence = fields.Integer(string='Sequence')

class Department(models.Model):
    _name='cap.department'
    _description = 'Department'

    name = fields.Char(string='Name')
    active = fields.Boolean(string='Active', default=True)
    sequence = fields.Integer(string='Sequence')


class ContactLocationRelationship(models.Model):
    _name='contact.location.relationship'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Contact Location Relationship'
    _order = 'sequence asc, id asc'

    name = fields.Char(string='Name', compute='_compute_name', readonly=True)
    active = fields.Boolean(string='Active', default=True)
    sequence = fields.Integer(string='Sequence')
    preferred_contact_method_ids = fields.Many2many('contact.method', 'contact_location_rel_contact_method_rel','location_contact_rel_id','contact_method_id',string='Preferred Contact Method')
    contact_id = fields.Many2one('res.partner', string='Contact', ondelete='set null', copy=True)
    contact_roles_ids = fields.Many2many('contact.role', 'contact_location_contact_role_rel', 'contact_location_rel_id', 'contact_role_id', string='Contact Roles')
    contact_email2 = fields.Char(related='contact_id.email', string='Contact Email2', store=True)
    contact_state_id = fields.Many2one('res.country.state', related='contact_id.state_id', string='Contact State', store=True)
    contact_name = fields.Char(related='contact_id.name', string='Name', store=True)
    contact_mobile = fields.Char(related='contact_id.mobile', string='Contact Mobile', store=True)
    contact_city = fields.Char(related='contact_id.city', string='Contact City', store=True)
    contact_phone = fields.Char(related='contact_id.phone', string='Contact Phone', store=True)
    contact_zip = fields.Char(related='contact_id.zip', string='Contact Zip', store=True)
    contact_email = fields.Char(related='contact_id.email', string='Contact Email', store=True)
    contact_street_2 = fields.Char(related='contact_id.street2', string='Contact Street 2', store=True)
    contact_country_id = fields.Many2one('res.country', related='contact_id.country_id', string='Contact Country', store=True)
    contact_street = fields.Char(related='contact_id.street', string='Contact Street', store=True)
    location_id = fields.Many2one('res.partner', string='Location', ondelete='set null', copy=True)
    location_type_id = fields.Many2one('location.type', string='Location Type', ondelete='set null')
    location_street_2 = fields.Char(related='location_id.street2', string='Location Street 2', store=True)
    location_state_id = fields.Many2one('res.country.state', related='location_id.state_id', string='Location State', store=True)
    location_zip = fields.Char(related='location_id.zip', string='Location Zip', store=True)
    location_type_1 = fields.Many2one('location.type', related='location_id.location_type_id', string='Location Type', store=True)
    location_street = fields.Char(related='location_id.street', string='Location Street', store=True)
    location_country_id = fields.Many2one('res.country', related='location_id.country_id', string='Location Country', store=True)
    location_type_2 = fields.Selection(related='location_id.partner_type', string='Location Type')
    location_city = fields.Char(related='location_id.city', string='Location City', store=True)
    new_location_country_id = fields.Many2one('res.country', string='New Location Country', ondelete='set null')
    new_location_state_id = fields.Many2one('res.country.state', string='New Location State', ondelete='set null')
    new_location_zip = fields.Char(string='New Location Zip')
    new_location_street_2 = fields.Char(string='New Location Street 2')
    new_location_city = fields.Char(string='New Location City')
    new_location_street = fields.Char(string='New Location Street')
    location_name = fields.Char(string='Location Name')
    pick_a_location = fields.Selection([('New Location', 'New Location'), ('Existing Location', 'Existing Location'), ('Same Address than the contact', 'Same Address than the contact')], string='Pick a location', default='New Location')
    relationship_type = fields.Selection([('Resident Owner', 'Resident Owner'), ('Tenant', 'Tenant'), ('Property Manager', 'Property Manager'), ('Landlord', 'Landlord'), ('Other Contact', 'Other Contact')] ,string='Relationship Type')
    
    @api.onchange('contact_id','location_id','relationship_type', 'location_name', 'pick_a_location', 'new_location_street')
    def _compute_name(self):
        for record in self:
            type = record.relationship_type if record.relationship_type != "" else "Undefined"
            location_name = record.location_name if record.location_name != "" else  record.location_street
            if not location_name:
                if record.pick_a_location == "Same Address than the contact":
                    location_name = record.contact_id.name
                if record.pick_a_location == "New Location":
                    location_name = record.new_location_street if record.new_location_street != "" else "Not yet defined"
                if record.pick_a_location == "Existing Location":
                    if not record.location_id:
                        location_name = "Waiting for selection"
                    else:
                        location_name = record.location_id.name
            record['name'] = "%s - %s - %s" % (record.contact_id.name, location_name, type)
    
    @api.model
    def create(self, vals):
        res = super(ContactLocationRelationship, self).create(vals)
        if vals.get('pick_a_location') == "Same Address than the contact":
            contact = res.contact_id
            location = self.env['res.partner'].create({
                'name':contact.name,	
                'street':contact.street,	
                'street2':contact.street2,	
                'city':contact.city,	
                'state_id':contact.state_id.id,
                'zip':contact.zip,	
                'country_id':contact.country_id.id,	
                'phone':contact.phone,	
                'email':contact.email,
                'partner_type': 'location'
            })
            res['location_id'] = location
            res['pick_a_location'] = "Existing Location"
            res['location_street'] = location.street
            res['location_city'] = location.city
            res['location_state_id'] = location.state_id.id
            res['location_zip'] = location.zip
        return res
