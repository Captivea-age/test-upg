from odoo import models, fields, api


class FurnaceComponents(models.Model):

    _name = "pm.furnace.component"

    pm_system_id = fields.Many2one("preventive_maintenance.system", string="System")

    furnace_bool = fields.Boolean(string="Furnace")
    furnace_component_name = fields.Many2one("preventive_maintenance.component",string="Component Name")
    furnace_section_id = fields.Many2one("preventive_maintenance.section", string="Component Section")
    furnace_component_sub_category = fields.Char(related="furnace_component_name.component_sub_category",string="Component Sub Category")
    furnace_service_life = fields.Integer(related="furnace_component_name.service_life",string="Service Life")
    furnace_equipment_id = fields.Many2one("preventive_maintenance.equipment",string="Equipment")
    component_state = fields.Selection([('good','Good'),('warning','Warning'),('error','Error')],string="Component Health")
    last_test = fields.Date(string="Last test date")
    install_date = fields.Date(string="Install date")

    brand_id = fields.Many2one("preventive_maintenance.brand",string="Brand")
    #model_id = fields.Many2one("preventive_maintenance.brand.model",string="Model")
    model_id = fields.Char(string="Model")
    serial_number = fields.Char("Serial #")   

    @api.onchange('furnace_bool')
    def _onchange_furnace_bool(self):
        furnace_component_name = False
        furnace_section_id = self.env['preventive_maintenance.section'].search([('name','=','Furnace')], limit=1).id or False
        res = {}
        res['domain'] = {'furnace_section_id': [('id','=',furnace_section_id)] or False}
        return res

    @api.onchange('furnace_equipment_id')
    def _onchange_furnace_equipment_id(self):
        furnace_section_id = self.env['preventive_maintenance.section'].search([('name','=','Furnace')], limit=1).id or False
        furnace_component_ids = self.env['preventive_maintenance.component'].search([('section_id','=',furnace_section_id)])
        component_ids = []
        for comp_id in furnace_component_ids:
            if self.furnace_equipment_id.id in comp_id.component_options.ids:
                component_ids.append(comp_id.id)
            elif not comp_id.component_options:
                component_ids.append(comp_id.id)
        res = {}
        res['domain'] = {'furnace_component_name': [('id', 'in', component_ids)]}
        return res

class CondenserComponents(models.Model):

    _name = "pm.condenser.component"

    pm_system_id = fields.Many2one("preventive_maintenance.system", string="System")

    condenser_bool = fields.Boolean(string="Condenser")
    condenser_component_name = fields.Many2one("preventive_maintenance.component",string="Component Name")
    condenser_section_id = fields.Many2one("preventive_maintenance.section", string="Component Section")
    condenser_component_sub_category = fields.Char(related="condenser_component_name.component_sub_category",string="Component Sub Category")
    condenser_service_life = fields.Integer(related="condenser_component_name.service_life",string="Service Life")
    condenser_equipment_id = fields.Many2one("preventive_maintenance.equipment",string="Equipment")
    component_state = fields.Selection([('good','Good'),('warning','Warning'),('error','Error')],string="Component Health")
    last_test = fields.Date(string="Last test date")
    install_date = fields.Date(string="Install date")
    

    brand_id = fields.Many2one("preventive_maintenance.brand",string="Brand")
    #model_id = fields.Many2one("preventive_maintenance.brand.model",string="Model")
    model_id = fields.Char(string="Model")
    serial_number = fields.Char("Serial #")    

    @api.onchange('condenser_bool')
    def _onchange_condenser_bool(self):
        condenser_component_name = False
        condenser_section_id = self.env['preventive_maintenance.section'].search([('name','=','Condenser')], limit=1).id or False
        res = {}
        res['domain'] = {'condenser_section_id': [('id','=',condenser_section_id)] or False}
        return res

    @api.onchange('condenser_equipment_id')
    def _onchange_condenser_equipment_id(self):
        condenser_section_id = self.env['preventive_maintenance.section'].search([('name','=','Condenser')], limit=1).id or False
        condenser_component_ids = self.env['preventive_maintenance.component'].search([('section_id','=',condenser_section_id)])
        component_ids = []
        for comp_id in condenser_component_ids:
            if self.condenser_equipment_id.id in comp_id.component_options.ids:
                component_ids.append(comp_id.id)
            elif not comp_id.component_options:
                component_ids.append(comp_id.id)
        res = {}
        res['domain'] = {'condenser_component_name': [('id', 'in', component_ids)]}
        return res

class EvaporatorComponents(models.Model):

    _name = "pm.evaporator.component"

    pm_system_id = fields.Many2one("preventive_maintenance.system", string="System")

    evaporator_bool = fields.Boolean(string="Evaporator")
    evaporator_component_name = fields.Many2one("preventive_maintenance.component",string="Component Name")
    evaporator_section_id = fields.Many2one("preventive_maintenance.section", string="Component Section")
    evaporator_component_sub_category = fields.Char(related="evaporator_component_name.component_sub_category",string="Component Sub Category")
    evaporator_service_life = fields.Integer(related="evaporator_component_name.service_life",string="Service Life")
    evaporator_equipment_id = fields.Many2one("preventive_maintenance.equipment",string="Equipment")
    component_state = fields.Selection([('good','Good'),('warning','Warning'),('error','Error')],string="Component Health")
    last_test = fields.Date(string="Last test date")
    install_date = fields.Date(string="Install date")


    brand_id = fields.Many2one("preventive_maintenance.brand",string="Brand")
    #model_id = fields.Many2one("preventive_maintenance.brand.model",string="Model")
    model_id = fields.Char(string="Model")
    serial_number = fields.Char("Serial #")


    @api.onchange('evaporator_bool')
    def _onchange_evaporator_bool(self):
        evaporator_component_name = False
        evaporator_section_id = self.env['preventive_maintenance.section'].search([('name','=','Evaporator')], limit=1).id or False
        res = {}
        res['domain'] = {'evaporator_section_id': [('id','=',evaporator_section_id)] or False}
        return res

    @api.onchange('evaporator_equipment_id')
    def _onchange_evaporator_equipment_id(self):
        evaporator_section_id = self.env['preventive_maintenance.section'].search([('name','=','Evaporator')], limit=1).id or False
        evaporator_component_ids = self.env['preventive_maintenance.component'].search([('section_id','=',evaporator_section_id)])
        component_ids = []
        for comp_id in evaporator_component_ids:
            if self.evaporator_equipment_id.id in comp_id.component_options.ids:
                component_ids.append(comp_id.id)
            elif not comp_id.component_options:
                component_ids.append(comp_id.id)
        res = {}
        res['domain'] = {'evaporator_component_name': [('id', 'in', component_ids)]}
        return res

class FancoilComponents(models.Model):

    _name = "pm.fancoil.component"

    pm_system_id = fields.Many2one("preventive_maintenance.system", string="System")

    fancoil_bool = fields.Boolean(string="FanCoil")
    fancoil_component_name = fields.Many2one("preventive_maintenance.component",string="Component Name")
    fancoil_section_id = fields.Many2one("preventive_maintenance.section", string="Component Section")
    fancoil_component_sub_category = fields.Char(related="fancoil_component_name.component_sub_category",string="Component Sub Category")
    fancoil_service_life = fields.Integer(related="fancoil_component_name.service_life",string="Service Life")
    fancoil_equipment_id = fields.Many2one("preventive_maintenance.equipment",string="Equipment")
    component_state = fields.Selection([('good','Good'),('warning','Warning'),('error','Error')],string="Component Health")
    last_test = fields.Date(string="Last test date")
    install_date = fields.Date(string="Install date")
    

    brand_id = fields.Many2one("preventive_maintenance.brand",string="Brand")
    #model_id = fields.Many2one("preventive_maintenance.brand.model",string="Model")
    model_id = fields.Char(string="Model")
    serial_number = fields.Char("Serial #")


    @api.onchange('fancoil_bool')
    def _onchange_fancoil_bool(self):
        fancoil_component_name = False
        fancoil_section_id = self.env['preventive_maintenance.section'].search([('name','=','Fancoil')], limit=1).id or False
        res = {}
        res['domain'] = {'fancoil_section_id': [('id','=',fancoil_section_id)] or False}
        return res

    @api.onchange('fancoil_equipment_id')
    def _onchange_fancoil_equipment_id(self):
        fancoil_section_id = self.env['preventive_maintenance.section'].search([('name','=','Fancoil')], limit=1).id or False
        fancoil_component_ids = self.env['preventive_maintenance.component'].search([('section_id','=',fancoil_section_id)])
        component_ids = []
        for comp_id in fancoil_component_ids:
            if self.fancoil_equipment_id.id in comp_id.component_options.ids:
                component_ids.append(comp_id.id)
            elif not comp_id.component_options:
                component_ids.append(comp_id.id)
        res = {}
        res['domain'] = {'fancoil_component_name': [('id', 'in', component_ids)]}
        return res

class ThermostatComponents(models.Model):

    _name = "pm.thermostat.component"

    pm_system_id = fields.Many2one("preventive_maintenance.system", string="System")

    thermostat_bool = fields.Boolean(string="Thermostat")
    thermostat_component_name = fields.Many2one("preventive_maintenance.component",string="Component Name")
    thermostat_section_id = fields.Many2one("preventive_maintenance.section", string="Component Section")
    thermostat_component_sub_category = fields.Char(related="thermostat_component_name.component_sub_category",string="Component Sub Category")
    thermostat_service_life = fields.Integer(related="thermostat_component_name.service_life",string="Service Life")
    thermostat_equipment_id = fields.Many2one("preventive_maintenance.equipment",string="Equipment")
    component_state = fields.Selection([('good','Good'),('warning','Warning'),('error','Error')],string="Component Health")
    last_test = fields.Date(string="Last test date")
    install_date = fields.Date(string="Install date")
    

    brand_id = fields.Many2one("preventive_maintenance.brand",string="Brand")
    #model_id = fields.Many2one("preventive_maintenance.brand.model",string="Model")
    model_id = fields.Char(string="Model")
    serial_number = fields.Char("Serial #")


    @api.onchange('thermostat_bool')
    def _onchange_thermostat_bool(self):
        thermostat_component_name = False
        thermostat_section_id = self.env['preventive_maintenance.section'].search([('name','=','Thermostat')], limit=1).id or False
        res = {}
        res['domain'] = {'thermostat_section_id': [('id','=',thermostat_section_id)] or False}
        return res

    @api.onchange('thermostat_equipment_id')
    def _onchange_thermostat_equipment_id(self):
        thermostat_section_id = self.env['preventive_maintenance.section'].search([('name','=','Thermostat')], limit=1).id or False
        thermostat_component_ids = self.env['preventive_maintenance.component'].search([('section_id','=',thermostat_section_id)])
        component_ids = []
        for comp_id in thermostat_component_ids:
            if self.thermostat_equipment_id.id in comp_id.component_options.ids:
                component_ids.append(comp_id.id)
            elif not comp_id.component_options:
                component_ids.append(comp_id.id)
        res = {}
        res['domain'] = {'thermostat_component_name': [('id', 'in', component_ids)]}
        return res

class AirflowDuctingComponents(models.Model):

    _name = "pm.airflow.ducting.component"

    pm_system_id = fields.Many2one("preventive_maintenance.system", string="System")

    airflow_ducting_bool = fields.Boolean(string="Airflow & Ducting")
    airflow_ducting_component_name = fields.Many2one("preventive_maintenance.component",string="Component Name")
    airflow_ducting_section_id = fields.Many2one("preventive_maintenance.section", string="Component Section")
    airflow_ducting_component_sub_category = fields.Char(related="airflow_ducting_component_name.component_sub_category",string="Component Sub Category")
    airflow_ducting_service_life = fields.Integer(related="airflow_ducting_component_name.service_life",string="Service Life")
    airflow_ducting_equipment_id = fields.Many2one("preventive_maintenance.equipment",string="Equipment")
    component_state = fields.Selection([('good','Good'),('warning','Warning'),('error','Error')],string="Component Health")
    last_test = fields.Date(string="Last test date")
    install_date = fields.Date(string="Install date")


    brand_id = fields.Many2one("preventive_maintenance.brand",string="Brand")
    #model_id = fields.Many2one("preventive_maintenance.brand.model",string="Model")
    model_id = fields.Char(string="Model")
    serial_number = fields.Char("Serial #")


    @api.onchange('airflow_ducting_bool')
    def _onchange_airflow_ducting_bool(self):
        airflow_ducting_component_name = False
        airflow_ducting_section_id = self.env['preventive_maintenance.section'].search([('name','=','Airflow & Ducting')], limit=1).id or False
        res = {}
        res['domain'] = {'airflow_ducting_section_id': [('id','=',airflow_ducting_section_id)] or False}
        return res

    @api.onchange('airflow_ducting_equipment_id')
    def _onchange_airflow_ducting_equipment_id(self):
        airflow_ducting_section_id = self.env['preventive_maintenance.section'].search([('name','=','Airflow & Ducting')], limit=1).id or False
        airflow_ducting_component_ids = self.env['preventive_maintenance.component'].search([('section_id','=',airflow_ducting_section_id)])
        component_ids = []
        for comp_id in airflow_ducting_component_ids:
            if self.airflow_ducting_equipment_id.id in comp_id.component_options.ids:
                component_ids.append(comp_id.id)
            elif not comp_id.component_options:
                component_ids.append(comp_id.id)
        res = {}
        res['domain'] = {'airflow_ducting_component_name': [('id', 'in', component_ids)]}
        return res

class BlowerComponents(models.Model):

    _name = "pm.blower.component"

    pm_system_id = fields.Many2one("preventive_maintenance.system", string="System")

    blower_bool = fields.Boolean(string="Blower")
    blower_component_name = fields.Many2one("preventive_maintenance.component",string="Component Name")
    blower_section_id = fields.Many2one("preventive_maintenance.section", string="Component Section")
    blower_component_sub_category = fields.Char(related="blower_component_name.component_sub_category",string="Component Sub Category")
    blower_service_life = fields.Integer(related="blower_component_name.service_life",string="Service Life")
    blower_equipment_id = fields.Many2one("preventive_maintenance.equipment",string="Equipment")
    component_state = fields.Selection([('good','Good'),('warning','Warning'),('error','Error')],string="Component Health")
    last_test = fields.Date(string="Last test date")
    install_date = fields.Date(string="Install date")
    

    brand_id = fields.Many2one("preventive_maintenance.brand",string="Brand")
    #model_id = fields.Many2one("preventive_maintenance.brand.model",string="Model")
    model_id = fields.Char(string="Model")
    serial_number = fields.Char("Serial #")


    @api.onchange('blower_bool')
    def _onchange_blower_bool(self):
        blower_component_name = False
        blower_section_id = self.env['preventive_maintenance.section'].search([('name','=','Blower')], limit=1).id or False
        res = {}
        res['domain'] = {'blower_section_id': [('id','=',blower_section_id)] or False}
        return res

    @api.onchange('blower_equipment_id')
    def _onchange_blower_equipment_id(self):
        blower_section_id = self.env['preventive_maintenance.section'].search([('name','=','Blower')], limit=1).id or False
        blower_component_ids = self.env['preventive_maintenance.component'].search([('section_id','=',blower_section_id)])
        component_ids = []
        for comp_id in blower_component_ids:
            if self.blower_equipment_id.id in comp_id.component_options.ids:
                component_ids.append(comp_id.id)
            elif not comp_id.component_options:
                component_ids.append(comp_id.id)
        res = {}
        res['domain'] = {'blower_component_name': [('id', 'in', component_ids)]}
        return res

class WaterDrainageComponents(models.Model):

    _name = "pm.water.drainage.component"

    pm_system_id = fields.Many2one("preventive_maintenance.system", string="System")

    water_drainage_bool = fields.Boolean(string="Water & Drainage")
    water_drainage_component_name = fields.Many2one("preventive_maintenance.component",string="Component Name")
    water_drainage_section_id = fields.Many2one("preventive_maintenance.section", string="Component Section")
    water_drainage_component_sub_category = fields.Char(related="water_drainage_component_name.component_sub_category",string="Component Sub Category")
    water_drainage_service_life = fields.Integer(related="water_drainage_component_name.service_life",string="Service Life")
    water_drainage_equipment_id = fields.Many2one("preventive_maintenance.equipment",string="Equipment")
    component_state = fields.Selection([('good','Good'),('warning','Warning'),('error','Error')],string="Component Health")
    last_test = fields.Date(string="Last test date")
    install_date = fields.Date(string="Install date")
    

    brand_id = fields.Many2one("preventive_maintenance.brand",string="Brand")
    #model_id = fields.Many2one("preventive_maintenance.brand.model",string="Model")
    model_id = fields.Char(string="Model")
    serial_number = fields.Char("Serial #")


    @api.onchange('water_drainage_bool')
    def _onchange_water_drainage_bool(self):
        water_drainage_component_name = False
        water_drainage_section_id = self.env['preventive_maintenance.section'].search([('name','=','Water & Drainage')], limit=1).id or False
        res = {}
        res['domain'] = {'water_drainage_section_id': [('id','=',water_drainage_section_id)] or False}
        return res

    @api.onchange('water_drainage_equipment_id')
    def _onchange_water_drainage_equipment_id(self):
        water_drainage_section_id = self.env['preventive_maintenance.section'].search([('name','=','Water & Drainage')], limit=1).id or False
        water_drainage_component_ids = self.env['preventive_maintenance.component'].search([('section_id','=',water_drainage_section_id)])
        component_ids = []
        for comp_id in water_drainage_component_ids:
            if self.water_drainage_equipment_id.id in comp_id.component_options.ids:
                component_ids.append(comp_id.id)
            elif not comp_id.component_options:
                component_ids.append(comp_id.id)
        res = {}
        res['domain'] = {'water_drainage_component_name': [('id', 'in', component_ids)]}
        return res

class IAQComponents(models.Model):

    _name = "pm.iaq.component"

    pm_system_id = fields.Many2one("preventive_maintenance.system", string="System")

    iaq_bool = fields.Boolean(string="IAQ")
    iaq_component_name = fields.Many2one("preventive_maintenance.component",string="Component Name")
    iaq_section_id = fields.Many2one("preventive_maintenance.section", string="Component Section")
    iaq_component_sub_category = fields.Char(related="iaq_component_name.component_sub_category",string="Component Sub Category")
    iaq_service_life = fields.Integer(related="iaq_component_name.service_life",string="Service Life")
    iaq_equipment_id = fields.Many2one("preventive_maintenance.equipment",string="Equipment")
    component_state = fields.Selection([('good','Good'),('warning','Warning'),('error','Error')],string="Component Health")
    last_test = fields.Date(string="Last test date")
    install_date = fields.Date(string="Install date")
    

    brand_id = fields.Many2one("preventive_maintenance.brand",string="Brand")
    #model_id = fields.Many2one("preventive_maintenance.brand.model",string="Model")
    model_id = fields.Char(string="Model")
    serial_number = fields.Char("Serial #")


    @api.onchange('iaq_bool')
    def _onchange_iaq_bool(self):
        iaq_component_name = False
        iaq_section_id = self.env['preventive_maintenance.section'].search([('name','=','IAQ')], limit=1).id or False
        res = {}
        res['domain'] = {'iaq_section_id': [('id','=',iaq_section_id)] or False}
        return res

    @api.onchange('iaq_equipment_id')
    def _onchange_iaq_equipment_id(self):
        iaq_section_id = self.env['preventive_maintenance.section'].search([('name','=','IAQ')], limit=1).id or False
        iaq_component_ids = self.env['preventive_maintenance.component'].search([('section_id','=',iaq_section_id)])
        component_ids = []
        for comp_id in iaq_component_ids:
            if self.iaq_equipment_id.id in comp_id.component_options.ids:
                component_ids.append(comp_id.id)
            elif not comp_id.component_options:
                component_ids.append(comp_id.id)
        res = {}
        res['domain'] = {'iaq_component_name': [('id', 'in', component_ids)]}
        return res
