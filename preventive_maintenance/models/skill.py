

from odoo import models, fields, api, _


class Skill(models.Model):
    
    _name = "preventive_maintenance.skill"
    _description = "Skill level model"
    
    name = fields.Char(string="Name")
    level = fields.Selection([('easy','Easy'),('normal','Normal'),('hard','Hard')], string="Skill level")

    