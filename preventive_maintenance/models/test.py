

from odoo import models, fields, api, _


class Test(models.Model):

    _name = "preventive_maintenance.test"
    _description = "Test type model"

    name = fields.Char(string="Test Type")
    units = fields.Selection([('pfw','Pass, Fail, Warn, N/A'),('volts','Volts'),('millivolts','Millivolts'),('psi','PSI'),('amp','Amp'),('microamps','Microamps'),('microfarad','Microfarad'),('rating','Rating'),('farenheit','Fahrenheit')], string="Units / Choice")
    lower_limit = fields.Char(string="Lower Limit")
    upper_limit = fields.Char("Upper Limit")
