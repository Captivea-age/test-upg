# -*- coding: utf-8 -*-
import logging
import requests
import json
import time
# from requests.auth import HTTPBasicAuth
from requests.structures import CaseInsensitiveDict
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
_logger = logging.getLogger(__name__)

class Task(models.Model):
    
    _inherit='project.task'
    
    job_titan_id = fields.Integer(string='Quotation Builder ST Job ID')
    url_job_service_titan = fields.Char(string='Quotation Builder ST Url')
    button_job_service_titan = fields.Char(string='Quotation Builder ST button', readonly=True)
    
    def customerCreation(self):
#         if not self.job_titan_id or not self.url_job_service_titan:
#             try:

                # Datas settings for all request
                headers = CaseInsensitiveDict()
                headers["Host"] = "api.servicetitan.com"
                headers["Content-Type"] = "application/json"
                headers["X-HTTP-ServiceTitan-Api-Key"] = "f9972f37-5545-4831-a22d-f2d23daab165"
                headers["Cookie"] = "st_authenticated_user=1; st_tenant=comfortmonster"
                headers["Authorization"] = "Bearer f9972f37-5545-4831-a22d-f2d23daab165"
                # end settings

                # Create Customer in Service Titan
                url_customer = "https://api.servicetitan.com/v1/customers"

                try:
                    customer_street_name = "Not Specified"
                    customer_street_unit = "Not Specified"
                    if self.customer_name and self.customer_name.street:
                        customer_street_split = self.customer_name.street.split(" ", 1)
                        customer_street_unit = str(customer_street_split[0])
                        customer_street_name = str(customer_street_split[1])
                except:
                    raise UserError("Customer Address needed")
                    
                try:
                    customer_email = "No email Specified"
                    if self.customer_email:
                        if (self.customer_email.find(",")) != -1:
                            customer_email_split = str(self.customer_email).split(",", 1)
                            customer_email = str(customer_email_split[0])
                        else:
                            customer_email = str(self.customer_email)
                except:
                    raise UserError("Customer Email Error, please verify it's well formed")
                
                name = "No name Specified"
                if self.customer_name and self.customer_name.name:
                    name = str(self.customer_name.name)
                location_type_related = "No location type Specified"
                if self.location_type_related:
                    location_type_related = str(self.location_type_related)
                country = "No country Specified"
                if self.customer_name and self.customer_name.country_id and self.customer_name.country_id.name:
                    country = str(self.customer_name.country_id.name)
                city = "No city Specified"
                if self.customer_name and self.customer_name.city:
                    city = str(self.customer_name.city)
                state = "No state Specified"
                if self.customer_name and self.customer_name.state_id and self.customer_name.state_id.name:
                    state = str(self.customer_name.state_id.name)
                zip = "No zip Specified"
                if self.customer_name and self.customer_name.zip:
                    zip = str(self.customer_name.zip)
                location_name = "No location name Specified"
                if self.partner_id and self.partner_id.name:
                    location_name = str(self.partner_id.name)
                location_street = "No location street Specified"
                if self.partner_id and self.partner_id.street:
                    location_street = str(self.partner_id.street)
                location_street2 = "No location street 2 Specified"
                if self.partner_id and self.partner_id.street2:
                    location_street2 = str(self.partner_id.street2)
                location_country = "No location country Specified"
                if self.partner_id and self.partner_id.country_id and self.partner_id.country_id.name:
                    location_country = str(self.partner_id.country_id.name)
                location_city = "No location city Specified"
                if self.partner_id.city and self.partner_id.city:
                    location_city = str(self.partner_id.city)
                location_state = "No location state Specified"
                if self.partner_id and self.partner_id.state_id and self.partner_id.state_id.name:
                    location_state = str(self.partner_id.state_id.name)
                location_zip = "No location zip Specified"
                if self.partner_id and self.partner_id.zip:
                    location_zip = str(self.partner_id.zip)
                contact_phone = "No partner phone Specified"
                if self.partner_id and self.partner_id.phone:
                    contact_phone = str(self.partner_id.phone)
                customer_phone = "No customer phone Specified"
                if self.customer_name and self.customer_name.phone:
                    customer_phone = str(self.customer_name.phone)                    
                    
                data_customer = """
                {
                    "name": \"""" + name + """\",
                    "balance": "0",
                    "doNotMail": "true",
                    "doNotService": "true",
                    "type": \"""" + location_type_related + """\",
                    "address": {
                        "street":\"""" + customer_street_name + """\",
                        "unit": \"""" + customer_street_unit + """\",
                        "country": \"""" + country + """\",
                        "city": \"""" + city + """\",
                        "state": \"""" + state + """\",
                        "zip": \"""" + zip + """\"
                    },
                    "locations": [
                        {
                        "name": \"""" + location_name + """\",
                        "address": {
                        "street":\"""" + location_street + """\",
                            "unit": \"""" + location_street2 + """\",
                            "country": \"""" + location_country + """\",
                            "city": \"""" + location_city + """\",
                            "state": \"""" + location_state + """\",
                            "zip": \"""" + location_zip + """\"
                        },
                        "contacts": [
                            {
                            "type": "Phone",
                            "value": \"""" + contact_phone + """\",
                            "memo": "null" 
                            }
                        ]
                        }
                    ],
                    "contacts": [
                        {
                        "type": "Phone",
                        "value": \"""" + customer_phone + """\",
                        "memo": "null"
                        },
                        {
                        "type": "Email",
                        "value": \"""" + customer_email + """\",
                        "memo": "null"
                        }
                    ]
                }
                """          
                request_customer = requests.post(url_customer, headers=headers, data=data_customer)
                _logger.warning((str(request_customer)))
                try:
                    customer_st_id = request_customer.json()["data"]["id"]
                except:
                    raise UserError("Request failed : Customer Malformed Data : %s || Please, verify your data before sending request" % (str(request_customer.content)))

                # Use for testing get the customer created
    #             url_customer_test = url_customer + "/" + str(customer_st_id)
    #             r = requests.get(url_customer_test, headers=headers)
    #             raise UserError("Test API (url: %s) : %s" % (url_customer_test,str(r.json())))
                # end test

                # END Create Customer in Service Titan

                # Create Location in Service Titan
                url_location = "https://api.servicetitan.com/v1/locations"

                try:
                    location_street_name = "Not Specified"
                    location_street_unit = "Not Specified"
                    if self.partner_id and self.partner_id.street:
                        location_street_split = self.partner_id.street.split(" ", 1)
                        location_street_unit = str(location_street_split[0])
                        location_street_name = str(location_street_split[1])
                except:
                    raise UserError("Location Address needed")

                phone_number_unique = False
                if self.partner_id.phone_number_ids:
                    phone_number_unique = self.partner_id.phone_number_ids[0].phone
                    
                location_name = "No location name Specified"
                if self.partner_id and self.partner_id.name:
                    location_name = str(self.partner_id.name)
                customer_name = "No customer name Specified"
                if self.customer_name and self.customer_name.name:
                    customer_name = str(self.customer_name.name)
                customer_country = "No customer country Specified"
                if self.customer_name and self.customer_name.country_id and self.customer_name.country_id.name:
                    customer_country = str(self.customer_name.country_id.name)
                customer_city = "No customer city Specified"
                if self.customer_name and self.customer_name.city:
                    customer_city = str(self.customer_name.city)
                customer_state = "No customer state Specified"
                if self.customer_name and self.customer_name.state_id and self.customer_name.state_id.name:
                    customer_state = str(self.customer_name.state_id.name)
                customer_zip = "No customer zip Specified"
                if self.customer_name and self.customer_name.zip:
                    customer_zip = str(self.customer_name.zip)  
                location_country = "US"
                if self.partner_id and self.partner_id.country_id and self.partner_id.country_id.name:
                    location_country = str(self.partner_id.country_id.name)
                location_city = "No location city Specified"
                if self.partner_id and self.partner_id.city:
                    location_city = str(self.partner_id.city)
                location_state = "No location state Specified"
                if self.partner_id and self.partner_id.state_id.name and self.partner_id.state_id.name:
                    location_state = str(self.partner_id.state_id.name)
                location_zip = "No location zip Specified"
                if self.partner_id and self.partner_id.zip:
                    location_zip = str(self.partner_id.zip)
                    

                data_location = """
                {
                  "name": \"""" + location_name + """\",
                  "customerId":  """+ str(customer_st_id) +""",
                  "customer": {
                    "name": \"""" + customer_name + """\",
                    "balance": 0,
                    "doNotMail": true,
                    "address": {
                        "street":\"""" + customer_street_name + """\",
                        "unit": \"""" + customer_street_unit + """\",
                        "country": \"""" + customer_country + """\",
                        "city": \"""" + customer_city + """\",
                        "state": \"""" + customer_state + """\",
                        "zip": \"""" + customer_zip + """\"
                    },
                    "doNotService": true,
                    "type": "Residential",
                    "contacts": [
                      {
                        "id": 0,
                        "type": "string",
                        "value": "string",
                        "memo": "string"
                      }
                    ]
                  },
                  "address": {
                        "street":\"""" + location_street_name + """\",
                        "unit": \"""" + location_street_unit + """\",
                        "country": \"""" + location_country + """\",
                        "city": \"""" + location_city + """\",
                        "state": \"""" + location_state + """\",
                        "zip": \"""" + location_zip + """\"
                    },
                  "contacts": [
                        {
                        "type": "Phone",
                        "value": \"""" + str(phone_number_unique) + """\",
                        "memo": "null"
                        },
                    ],
                  "isCustomerTheSameAsLocation": true,
                  "equipment": [
                  ]
                }
                """

                request_location = requests.post(url_location, headers=headers, data=data_location)
                _logger.warning((str(request_location)))
                try:
                    location_st_id = request_location.json()["data"]["id"]
                    contact_st_id = request_location.json()["data"]["customer"]["contacts"][0]["id"]
                except:
                    raise UserError("Request failed : Location Malformed Data : %s || Please, verify your data before sending request" % (str(request_location.content)))

                # Use for testing get the location created
    #             url_location_test = url_location + "/" + str(location_st_id)
    #             r = requests.get(url_location_test, headers=headers)
    #             raise UserError("Test API (url: %s) : %s" % (url_location_test,str(r.json())))
                # end test

                # END Create Location in Service Titan

                # Create Job in Service Titan

                url_job = "https://api.servicetitan.com/v1/jobs"

                try:
                    datetime_start = self.planned_date_begin.isoformat()
                    datetime_end = self.planned_date_end.isoformat()
                except:
                    raise UserError("Date start or end not set, cant create a job without")

                data_job = """
                {
                    "start": \"""" + str(datetime_start) + """\",
                    "end": \"""" + str(datetime_end) + """\",
                    "businessUnit": 18993,
                    "jobType": 57268790,
                    "arrivalWindowStart": \"""" + str(datetime_start) + """\",
                    "arrivalWindowEnd": \"""" + str(datetime_end) + """\",
                    "customer": {
                        "id": \"""" + str(customer_st_id) + """\",
                        "contacts": [
                        {
                            "id": \"""" + str(contact_st_id) + """\",
                        }
                        ]
                    },
                    "location": {
                        "id": \"""" + str(location_st_id) + """\",
                    },
                    "summary": "Test Entry of a job",
                    "tags": []
                }

                """

                request_job = requests.post(url_job, headers=headers, data=data_job)
                _logger.warning((str(request_job)))

                try:
                    job_st_id = request_job.json()["data"]["id"]
                except:
                    raise UserError("Request failed : Job Malformed Data : %s || Please, verify your data before sending request" % (str(request_job.content)))

                # Use for testing get the customer created
    #             url_job_test = url_job + "/" + str(59128635)
    #             r = requests.get(url_job_test, headers=headers)
    #             raise UserError("Test API (url: %s) : %s" % (url_job_test,str(r.content)))
                # end test

                # END Create Location in Service Titan

                self['job_titan_id'] = int(job_st_id)
                self['url_job_service_titan'] = "https://quotes.comfortmonster.com/tech/job/%s" % str(job_st_id)
                self['button_job_service_titan'] = "<a target='_blank' href='%s' class='btn btn-secondary'>Quotation Builder</a>" % (self['url_job_service_titan'])
#             except:
#                 raise UserError("Request failed")

#         return request.post('https:/quotes.comfortmonster.com/tech/job/59149641')
        
#         return {
#             'type': 'ir.actions.act_url',
# #             'url': self['url_job_service_titan'],
#             'url': 'https:/quotes.comfortmonster.com/tech/job/59149641'
#             'target': 'new',
#         }
        