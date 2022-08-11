from odoo import models, fields, api, _

class AirflowComponent(models.Model):

    _name = "pm.component.airflow"
    _desc = "Airflow component"

    name = fields.Char(string="Name")
    airflow_component_type = fields.Many2one('pm.component.airflow.type',string="Airflow component type")
    cfm = fields.Integer(string="Cubic Feet per Minute")
    filter_coefficient = fields.Float(string="Filter Coefficient")
  
class AirflowComponentRecord(models.Model):

    _name = "pm.component.airflow.record"
    _desc = "Airflow component record"
    # _rec_name = "airflow_component.name"

    # name = fields.Char(string="Name")
    airflow_component = fields.Many2one('pm.component.airflow',string="Airflow component")

    supply_or_return = fields.Selection(related="airflow_component.airflow_component_type.supply_or_return",string="Supply or Return")
    pm_system_id = fields.Many2one('preventive_maintenance.system',string="System ID")
    cfm = fields.Integer(related="airflow_component.cfm", string="Cubic Feet per Minute")
    filter_coefficient = fields.Float(related="airflow_component.filter_coefficient", string="Filter Coefficient")
    # pm_component_airflow_id = fields.Many2one("preventive_maintenance.system", string="Airflow Component")
    
    def add_airflow_supply_component(self):
        
        return self

    def add_airflow_return_component(self):
        
        return self


class AirflowComponentType(models.Model):

    _name = "pm.component.airflow.type"
    _desc = "Airflow component type"

    name = fields.Char(string="Name")
    supply_or_return = fields.Selection([('supply','Supply'),('return','return'),('both','Both'),('na','N/A'),],string="Supply or Return")    

class AirflowComponentTypeOld(models.Model):

    _name = "preventive_maintenance.component.airflow.type"
    _desc = "do not use this class"
