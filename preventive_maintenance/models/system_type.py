

from odoo import models, fields, api, _


class SystemType(models.Model):
    
    _name = "preventive_maintenance.system_type"
    _description = "System type model"
    
    name = fields.Char(string="System Type")
    abbreviation = fields.Char(string="Abbreviation")
    category = fields.Selection([('ac','AC'),('hp','HP')], string="Category")
 
    furnace_bool = fields.Boolean(string="Furnace")
    condenser_bool = fields.Boolean(string="Condenser")
    evaporator_bool = fields.Boolean(string="Evaporator")
    fancoil_bool = fields.Boolean(string="FanCoil")
    thermostat_bool = fields.Boolean(string="Thermostat")
    airflow_ducting_bool = fields.Boolean(string="Airflow & Ducting")
    blower_bool = fields.Boolean(string="Blower")
    water_drainage_bool = fields.Boolean(string="Water & Drainage")
    iaq_bool = fields.Boolean(string="IAQ")
    simple_name = fields.Char(string="Simple name")