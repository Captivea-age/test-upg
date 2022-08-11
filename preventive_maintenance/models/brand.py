from odoo import models, fields, api, _

class Brand(models.Model):
    
    _name = "preventive_maintenance.brand"
    _description = "Brand model"
    
    name = fields.Char(string="Name")
    sequence = fields.Integer(string="Sequence")


class ComponentModel(models.Model):
    _name = "preventive_maintenance.brand.model"

    name = fields.Char(string="Name")
    brand_id = fields.Many2one('preventive_maintenance.brand',string="Brand")
    sequence = fields.Integer(string="Sequence")
