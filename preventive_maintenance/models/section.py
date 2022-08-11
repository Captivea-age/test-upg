

from odoo import models, fields, api, _


class Section(models.Model):
    
    _name = "preventive_maintenance.section"
    _description = "Section model"
    
    name = fields.Char(string="Section Name")
    access_location = fields.Selection([('inside','Inside'),('outside','Outside')], string="Access Location")
