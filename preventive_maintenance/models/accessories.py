from odoo import models, fields, api, _


class Accessories(models.Model):
    
    _name = "pm.accessories.component"
    _description = "Accessories model"
    
    name = fields.Char(string="Name")
    brand = fields.Many2one("preventive_maintenance.brand",string="Brand")