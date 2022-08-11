# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import logging
logger = logging.getLogger(__name__)

class SearchPopup(models.Model):
    _name = 'search.popup'
    _description = 'Search Popup'

    search_field_name = fields.Char( string='Search name')
    search_field_email = fields.Char( string='Search email')
    search_field_phone = fields.Char( string='Search phone')
    search_field_address = fields.Char( string='Search address')

    location_diff = fields.Char()
    match_count = fields.Integer(string='Match count', default=0)
    possible_partner_domain = fields.Many2many('res.partner',readonly=True)
    possible_partner_id = fields.Many2one('res.partner' ,string="Possible match")
    current_partner_id = fields.Many2one('res.partner' ,string="Current partner")

    possible_partner_id_street = fields.Char(related='possible_partner_id.street', string='Partner Street', readonly=True)
    possible_partner_id_city = fields.Char(related='possible_partner_id.city', string='Partner City', readonly=True)
    possible_partner_id_phone = fields.Char(related='possible_partner_id.phone', string='Partner Landline', readonly=True)
    possible_partner_id_email = fields.Char(related='possible_partner_id.email', string='Partner Email', readonly=True)

    relationship_type = fields.Selection([('Resident Owner','Resident owner'),('Tenant','Tenant'),('Property Manager','Property manager'),('Landlord','Landlord'),('Other Contact','Other Contact')], string='Relationship type')
    contact_roles_ids = fields.Many2many('contact.role', 'search_popup_contact_role_rel', string='Contact roles')
    contact_method_ids = fields.Many2many('contact.method','search_popup_contact_method_rel', string='Contact methods')

    helpdesk_ticket_id = fields.Many2one('helpdesk.ticket')


    #@api.onchange('possible_partner_id')
    def _compute_partner_domain(self,result_list=False):
        for record in self:
            logger.warning('tried to create the domain')
            logger.warning('this is the search_result %s' %(str(result_list)))

            if result_list and len(result_list)>0:

                record.write({
                    'possible_partner_domain':[(6,0,result_list)]
                })

                logger.warning('partner domain : %s' %(str(record.possible_partner_domain)))

                return {
                    'possible_partner_domain':[(6,0,result_list)],
                }
            else:
                if record.possible_partner_domain != False:
                    return {
                        'possible_partner_domain':record.possible_partner_domain,
                    }  
                elif record.possible_partner_domain == False :                  
                    return {
                        'possible_partner_domain':record.possible_partner_domain,
                    }

    def partnerSearch(self):
        #Search for the partner or contact
        possible_partner_id = False
        result_list = []

        if self.search_field_name:
            search_result_name = self.env['res.partner'].search([('name','ilike',str(self.search_field_name)),('partner_type',self.location_diff,'location')])
        elif (self.search_field_address != False) and (self.search_field_name==False) :    
            search_result_name = self.env['res.partner'].search([('street','ilike',str(self.search_field_address)),('partner_type','=','location')])
        else:
            search_result_name = self.env['res.partner'].search([('partner_type',self.location_diff,'location')])
        
        search_result_email = self.env['res.partner'].search([('email','ilike',str(self.search_field_email)),('partner_type',self.location_diff,'location')])
        search_result_street = self.env['res.partner'].search([('street','ilike',str(self.search_field_address)),('partner_type',self.location_diff,'location')])
        search_result_main_phone = self.env['res.partner'].search(['&',('partner_type',self.location_diff,'location'),'|',('phone','ilike',str(self.search_field_phone)),('phone_number_ids.phone','ilike',str(self.search_field_phone))])
        #search_result_phone_numbers = self.env['res.partner'].search([('phone_number_ids','in',str(self.search_field_phone)),('x_studio_partner_type',self.location_diff,'location')])

        logger.info('Searched for %s in field %s: \n Result : %s' % (self.search_field_name, 'name', len(search_result_name))) 
        logger.info('Searched for %s in field %s: \n Result : %s' % (self.search_field_email, 'email', len(search_result_email))) 
        logger.info('Searched for %s in field %s: \n Result : %s' % (self.search_field_address, 'street', len(search_result_street))) 
        logger.info('Searched for %s in field %s: \n Result : %s' % (self.search_field_phone, 'phone', len(search_result_main_phone))) 
        #logger.info('Searched for %s in field %s: \n Result : %s' % (self.search_field_phone, 'phone_number_ids', len(search_result_phone_numbers))) 


        for partner in search_result_name:
            logger.info('Partner name:%s' % (str(partner.name)))
            test = False
            contact_validation = True

            #This allows to exclusively search, if there's data in one of those fields
            #If there's data in email search, tries to find a match
            if len(search_result_email)>0:
                contact_validation = False
                for partner_email in search_result_email:
                    if partner == partner_email:
                        contact_validation = True
                logger.info('Passed the email validation with contact_validation:'+str(contact_validation))
            #If there's data in street search, tries to find a match
            if len(search_result_street)>0:
                contact_validation = False
                for partner_street in search_result_street:
                    if partner == partner_street:
                        contact_validation = True
                logger.info('Passed the street validation with contact_validation:'+str(contact_validation))

            #If there's data in main phone search, tries to find a match
            if len(search_result_main_phone)>0:
                contact_validation = False
                for partner_phone in search_result_main_phone:
                    if partner == partner_phone:
                        contact_validation = True
                logger.info('Passed the phone validation with contact_validation:'+str(contact_validation))

            #If there's data in other phone search, tries to find a match
            # if len(search_result_phone_numbers)>0:
            #     contact_validation = False
            #     for partner_phone_list in search_result_phone_numbers:
            #         if partner == partner_phone_list:
            #             contact_validation = True
            #        logger.info('Passed the multiple phones validation with contact_validation:'+str(contact_validation))

            if contact_validation:
                result_list.append(partner.id)
                logger.info('Partner : %s was added to the potential partners list' %(str(partner.name)))


        self._compute_partner_domain(result_list)
        self.match_count = len(result_list)

        for partner in result_list:
            self.possible_partner_id = result_list[0]


        # If found, open popup with selected contact data in it
        if self.possible_partner_id:

            context = {
                'default_possible_partner_domain':self.possible_partner_domain
            }

            return {
                'type': 'ir.actions.act_window',
                'res_model': 'search.popup',
                'view': 'view.res.partner.search.popup',
                'view_mode':'form',
                'target': 'new',
                'res_id':self.id,
                'context':context,
                'domain':{'possible_partner_id': str(self.possible_partner_domain)}
            }


        # If not found, open popup with nothing
        else:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'search.popup',
                'view': 'view.res.partner.search.popup',
                'view_mode':'form',
                'target': 'new',
                'res_id':self.id,
            }

    def saveContactToLocation(self):

        contact = self.possible_partner_id
        location = self.current_partner_id

        relation = self.env['contact.location.relationship'].create({
            'name':('%s - %s - %s' % (str(contact.name),str(location.name),str(self.relationship_type))),
            'contact_id':contact.id,
            'location_id':location.id,
            'relationship_type':self.relationship_type,
            'pick_a_location':'Existing Location',
            'preferred_contact_method_ids': self.contact_method_ids,
            'contact_roles_ids':self.contact_roles_ids,

        })

        new_bill_to = False
        if self.contact_roles_ids:
            for role in self.contact_roles_ids:
                # Assume 'Bill to' role has ID 2
                if role.id == 2:
                    new_bill_to = True
        if new_bill_to:
            location['email'] = contact.email

        return True

    def saveContactToLocationAndNew(self):
        contact = self.possible_partner_id
        location = self.current_partner_id

        relation = self.env['contact.location.relationship'].create({
            'name':('%s - %s - %s' % (str(contact.name),str(location.name),str(self.relationship_type))),
            'contact_id':contact.id,
            'location_id':location.id,
            'relationship_type':self.relationship_type,
            'pick_a_location': 'Existing Location',
            'preferred_contact_method_ids':self.contact_method_ids,
            'contact_roles_ids':self.contact_roles_ids,


        })
        context = {
            'default_location_diff':'!=',
            'default_current_partner_id':self.current_partner_id.id
        }

        return {
                'type': 'ir.actions.act_window',
                'res_model': 'search.popup',
                'view': 'view.res.partner.search.popup',
                'view_mode':'form',
                'context':context,
                'target': 'new',
                #'res_id':,
            }

    def saveLocationToContact(self):
        location = self.possible_partner_id
        contact = self.current_partner_id

        relation = self.env['contact.location.relationship'].create({
            'name':('%s - %s - %s' % (str(contact.name),str(location.name),str(self.relationship_type))),
            'contact_id':contact.id,
            'location_id':location.id,
            'relationship_type':self.relationship_type,
            'pick_a_location':'Existing Location',
            'preferred_contact_method_ids':self.contact_method_ids,
            'contact_roles_ids':self.contact_roles_ids, 
        })
        return True

    def saveLocationToContactAndNew(self):
        location = self.possible_partner_id
        contact = self.current_partner_id

        relation = self.env['contact.location.relationship'].create({
            'name':('%s - %s - %s' % (str(contact.name),str(location.name),str(self.relationship_type))),
            'contact_id':contact.id,
            'location_id':location.id,
            'relationship_type':self.relationship_type,
            'pick_a_location':'Existing Location',
            'preferred_contact_method_ids':self.contact_method_ids,
            'contact_roles_ids':self.contact_roles_ids,
        })

        context = {
            'default_location_diff':'=',
            'default_current_partner_id':self.current_partner_id.id

        }

        return {
                'type': 'ir.actions.act_window',
                'res_model': 'search.popup',
                'view': 'view.res.partner.search.popup',
                'view_mode':'form',
                'context':context,
                'target': 'new',
                #'res_id':,
            }

    def openPartnerPopup(self):
        logger.info('Opened the new contact popup')

        if self.location_diff != "=":
            partner_type = 'person'
        else:
            partner_type = 'location'


        #Getting location or contact's address in case user was only looking for a name
        if not self.search_field_address:
            context_street = self.current_partner_id.street
            context_street2 = self.current_partner_id.street2
            context_city = self.current_partner_id.city
            context_zip = self.current_partner_id.zip
        else:
            context_street = self.search_field_address
            context_street2 = False
            context_city = False
            context_zip = False

        context = {
            'default_partner_type':partner_type,       
            'default_name' : self.search_field_name,
            'default_email' : self.search_field_email,
            'default_phone' : self.search_field_phone,
            'default_street' : context_street,
            'default_street2' : context_street2,
            'default_city' : context_city,
            'default_zip' : context_zip,
            'default_current_partner_id':self.current_partner_id.id,
            'default_location_type':1,
            'default_relationship_type':'Resident Owner',
            'default_contact_role':(6,0,[1,2]),
            'default_contact_method':(6,0,[1,2,3]),
        }

        view_form = self.env.ref('cap_contact.view_res_partner_form_simplified', False)

        return {
                'name' : 'New contact or location',
                'type' : 'ir.actions.act_window',
                'res_model': 'res.partner',
                'views': [(view_form.id, 'form')],
                'view_id': view_form.id,
                'view_mode':'form',
                'context':context,
                'target': 'new',
        }

  # Action used when creating a new relationship from Helpdesk view
    def savePartnerReturnHelpdesk(self):

        if self.possible_partner_id.partner_type == "location":
            location = self.possible_partner_id
            contact = self.current_partner_id
        else:
            location = self.current_partner_id
            contact = self.possible_partner_id

        relation = self.env['contact.location.relationship'].create({
            'name':('%s - %s - %s' % (str(contact.name),str(location.name),str(self.relationship_type))),
            'contact_id':contact.id,
            'location_id':location.id,
            'relationship_type':self.relationship_type,
            'pick_a_location':'Existing Location',
            'preferred_contact_method_ids':self.contact_method_ids,
            'contact_roles_ids':self.contact_roles_ids,            
        })

        self.helpdesk_ticket_id.write({
            'partner_id':relation.location_id.id,
            'customer_name':relation.contact.id,
            'pick_the_location_id':relation.id,
            'city':relation.location_city,
            'zip':relation.location_zip,
        })
        
        return {
                'type': 'ir.actions.act_window',
                'res_model': 'helpdesk.ticket',
                'view': 'helpdesk.helpdesk_ticket_view_form',
                'view_mode':'form',
                'res_id':self.helpdesk_ticket_id.id,
                'target': 'current',
            }
class ResPartner(models.Model):
    _inherit="res.partner"

    st_location_id = fields.Char(string='ST Location ID')
    st_customer_id = fields.Char(string='ST Customer ID')
    current_partner_id = fields.Many2one('res.partner', string='Current partner')
    relationship_type = fields.Selection([('Resident Owner','Resident owner'),('Tenant','Tenant'),('Property Manager','Property manager'),('Landlord','Landlord'),('Other Contact','Other Contact')], string='Relationship type')
    contact_roles_ids = fields.Many2many('contact.role', 'partner_contact_role_rel', string='Contact roles')
    contact_method_ids = fields.Many2many('contact.method','partner_contact_method_rel', string='Contact methods')

    helpdesk_ticket_id = fields.Many2one('helpdesk.ticket')

    def openContactPopup(self):

        context = {
            'default_location_diff':'!=',
            'default_current_partner_id':self.id,
            'default_relationship_type':'Resident Owner',
        }
        logger.info('Opened the contact popup')

        return {
                'type': 'ir.actions.act_window',
                'res_model': 'search.popup',
                'view': 'view.res.partner.search.popup',
                'view_mode':'form',
                'context':context,
                'target': 'new',
            }

    def openLocationPopup(self):

        context = {
            'default_location_diff':'=',
            'default_current_partner_id':self.id,
            'default_relationship_type':'Resident Owner',
        }
        logger.info('Opened the location popup')

        return {
                'type': 'ir.actions.act_window',
                'res_model': 'search.popup',
                'view': 'view.res.partner.search.popup',
                'view_mode':'form',
                'context':context,
                'target': 'new',
            }

    def savePartner(self):
        logger.info('Tried to save a new contact')
        if self.partner_type == "location":
            location = self
            contact = self.current_partner_id
        else:
            location = self.current_partner_id
            contact = self

        relation = self.env['contact.location.relationship'].create({
            'name':('%s - %s - %s' % (str(contact.name),str(location.name),str(self.relationship_type))),
            'contact_id':contact.id,
            'location_id':location.id,
            'relationship_type':self.relationship_type,
            'pick_a_location':'Existing Location',
            'preferred_contact_method_ids':self.contact_method_ids,
            'contact_roles_ids':self.contact_roles_ids,            
        })
        return True
