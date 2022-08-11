from odoo import models, fields

class ZIP(models.Model):
    _name = 'zip.list'
    _description = 'Zip selector for Team color'

    zip = fields.Char(string='Zip', required=True)
    team = fields.Many2one("team.color", string="Team", required=True)
