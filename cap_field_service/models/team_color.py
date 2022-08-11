from odoo import models, fields

class TeamColor(models.Model):
    _name="team.color"
    _description = 'Team color selection for Field Service'

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color", required=True)