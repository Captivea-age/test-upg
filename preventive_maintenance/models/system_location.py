

from odoo import models, fields, api, _


class SystemLocation(models.Model):
    
    _name = "preventive_maintenance.system_location"
    _description = "System location model"
    
    name = fields.Char(string="Name")
    access_location = fields.Selection([('inside','Inside'),('outside','Outside')], string="Access Location")
