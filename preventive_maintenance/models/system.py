from odoo import models, fields, api, _
import datetime
import logging
logger = logging.getLogger(__name__)
import json
from lxml import etree
from odoo.exceptions import AccessError, UserError, ValidationError

class System(models.Model):

    _name = "preventive_maintenance.system"
    _description = "Systems model"
    
    equipment_list = ['furnace','condenser','evaporator','thermostat','blower','water_drainage','iaq']
    equipment_list_id = ['furnace_equipment_id','condenser_equipment_id','evaporator_equipment_id','thermostat_equipment_id','blower_equipment_id','water_drainage_equipment_id','iaq_equipment_id']
    equipment_list_bool = ['furnace_bool','condenser_bool','evaporator_bool','thermostat_bool','blower_bool','water_drainage_bool','iaq_bool']
    list_brand = ['brand','furnace_equipment_brand_id','condenser_equipment_brand_id','evaporator_equipment_brand_id','fancoil_equipment_brand_id','thermostat_equipment_brand_id','blower_equipment_brand_id','water_drainage_equipment_brand_id','iaq_equipment_brand_id']

    name = fields.Char(string="Name")

    location_id = fields.Many2one("res.partner", string="Location")
    system_type_id = fields.Many2one("preventive_maintenance.system_type",string="System type")
    system_location_id = fields.Many2one("preventive_maintenance.system_location", string="System Location")
    first_install = fields.Date(string="First install date", readonly=True,compute="_compute_install_date")
    
    month_install = fields.Selection([('1','January'),('2','February'),('3','March'),('4','April'),('5','May'),('6','June'),('7','July'),('8','August'),('9','September'),('10','October'),('11','November'),('12','December')],string="Month")
    year_install = fields.Selection([('2022','2022'),('2021','2021'),('2020','2020'),('2019','2019'),('2018','2018'),('2017','2017'),('2016','2016'),('2015','2015'),('2014','2014'),('2013','2013'),('2012','2012'),('2011','2011'),('2010','2010'),('2009','2009'),('2008','2008'),('2007','2007'),('2006','2006'),('2005','2005'),('2004','2004'),('2003','2003'),('2002','2002'),('2001','2001'),('2000','2000'),('1999','1999'),('1998','1998'),('1997','1997'),('1996','1996'),('1995','1995'),('1994','1994'),('1993','1993'),('1992','1992'),('1991','1991'),('1990','1990')], string="Year")

    system_age = fields.Float(string='System age', compute='_compute_system_age',readonly=True,stored=False, digits=(3,1))
    brand = fields.Many2one("preventive_maintenance.brand",string="Brand")

    last_service = fields.Date(string="Last service date")
    next_service = fields.Date(string="Next service date")
    test_results = fields.One2many("preventive_maintenance.test.records","system_id",string="Test results")
    health = fields.Selection([('good','Good'),('warning','Warning'),('error','Error')],string="System Health",stored=False, compute='_compute_system_health')
    maintenance_ids = fields.One2many("preventive_maintenance.maintenance","system_id",string="Maintenance records")
    notification_status = fields.Selection([('none','None'),('pending','Pending'),('sent','Sent'),('dismissed','Dismissed'),('scheduled','Scheduled')],string="Notification status")
    notification_status_date = fields.Date(string="Last notification status change")
    monstercare_covered = fields.Boolean(string="Monstercare covered")
    base_risk_score = fields.Float(string="Risk score", default=1)
    active =  fields.Boolean(string="Active",default="True")
    helpdesk_ticket_id = fields.Many2one("helpdesk.ticket",string="Helpdesk ID", stored=False)

    maintenance_soon_needed  = fields.Boolean(string="Maintenance soon needed")
    maintenance_needed  = fields.Boolean(string="Maintenance Needed now")
    maintenance_created  = fields.Boolean(string="Maintenance created")

    service_area = fields.Selection([('first_floor','First Floor'),('second_floor','Second Floor'),('whole_house','Whole House'),('other','Other')], string="Service Area")
    service_area_custom = fields.Char(string="Other Service Area Name")
    subscription_id = fields.Many2one("sale.subscription",string="Membership ID")

    tons = fields.Selection([('1','1'),('1.5','1.5'),('2','2'),('2.5','2.5'),('3','3'),('3.5','3.5'),('4','4'),('4.5','4.5'),('5','5'),('5.5','5.5'),('6','6')], string="Tons")

    furnace_bool = fields.Boolean(string="Furnace")
    furnace_component_name = fields.Many2one("preventive_maintenance.component",string="Component Name")
    furnace_section_id = fields.Many2one("preventive_maintenance.section", string="Component Section")
    furnace_component_sub_category = fields.Char(related="furnace_component_name.component_sub_category",string="Component Sub Category")
    furnace_service_life = fields.Integer(related="furnace_component_name.service_life",string="Service Life")
    furnace_equipment_id = fields.Many2one("preventive_maintenance.equipment",string="Equipment")
    furnace_equipment_brand_id = fields.Many2one("preventive_maintenance.brand",string="Brand")
    furnace_equipment_model_id = fields.Char(string="Model")
    furnace_equipment_serial_number = fields.Char(string="Serial #")
    furnace_equipment_install_date =  fields.Date(string="Install date",readonly=True,compute="_compute_furnace_install_date")
    furnace_equipment_month_install = fields.Selection([('1','January'),('2','February'),('3','March'),('4','April'),('5','May'),('6','June'),('7','July'),('8','August'),('9','September'),('10','October'),('11','November'),('12','December')],string="Month")
    furnace_equipment_year_install = fields.Selection([('2022','2022'),('2021','2021'),('2020','2020'),('2019','2019'),('2018','2018'),('2017','2017'),('2016','2016'),('2015','2015'),('2014','2014'),('2013','2013'),('2012','2012'),('2011','2011'),('2010','2010'),('2009','2009'),('2008','2008'),('2007','2007'),('2006','2006'),('2005','2005'),('2004','2004'),('2003','2003'),('2002','2002'),('2001','2001'),('2000','2000'),('1999','1999'),('1998','1998'),('1997','1997'),('1996','1996'),('1995','1995'),('1994','1994'),('1993','1993'),('1992','1992'),('1991','1991'),('1990','1990')], string="Year")

    furnace_component_ids = fields.One2many("pm.furnace.component","pm_system_id",string="Furnace Components")

    condenser_bool = fields.Boolean(string="Condenser")
    condenser_component_name = fields.Many2one("preventive_maintenance.component",string="Component Name")
    condenser_section_id = fields.Many2one("preventive_maintenance.section", string="Component Section")
    condenser_component_sub_category = fields.Char(related="condenser_component_name.component_sub_category",string="Component Sub Category")
    condenser_service_life = fields.Integer(related="condenser_component_name.service_life",string="Service Life")
    condenser_equipment_id = fields.Many2one("preventive_maintenance.equipment",string="Equipment")
    condenser_equipment_brand_id = fields.Many2one("preventive_maintenance.brand",string="Brand")
    condenser_equipment_model_id = fields.Char(string="Model")
    condenser_equipment_serial_number = fields.Char(string="Serial #")
    condenser_equipment_install_date =  fields.Date(string="Install date",readonly=True,compute="_compute_condenser_install_date")
    condenser_equipment_month_install = fields.Selection([('1','January'),('2','February'),('3','March'),('4','April'),('5','May'),('6','June'),('7','July'),('8','August'),('9','September'),('10','October'),('11','November'),('12','December')],string="Month")
    condenser_equipment_year_install = fields.Selection([('2022','2022'),('2021','2021'),('2020','2020'),('2019','2019'),('2018','2018'),('2017','2017'),('2016','2016'),('2015','2015'),('2014','2014'),('2013','2013'),('2012','2012'),('2011','2011'),('2010','2010'),('2009','2009'),('2008','2008'),('2007','2007'),('2006','2006'),('2005','2005'),('2004','2004'),('2003','2003'),('2002','2002'),('2001','2001'),('2000','2000'),('1999','1999'),('1998','1998'),('1997','1997'),('1996','1996'),('1995','1995'),('1994','1994'),('1993','1993'),('1992','1992'),('1991','1991'),('1990','1990')], string="Year")

    condenser_component_ids = fields.One2many("pm.condenser.component","pm_system_id",string="Condenser Components")

    evaporator_bool = fields.Boolean(string="Evaporator")
    evaporator_component_name = fields.Many2one("preventive_maintenance.component",string="Component Name")
    evaporator_section_id = fields.Many2one("preventive_maintenance.section", string="Component Section")
    evaporator_component_sub_category = fields.Char(related="evaporator_component_name.component_sub_category",string="Component Sub Category")
    evaporator_service_life = fields.Integer(related="evaporator_component_name.service_life",string="Service Life")
    evaporator_equipment_id = fields.Many2one("preventive_maintenance.equipment",string="Equipment")
    evaporator_equipment_brand_id = fields.Many2one("preventive_maintenance.brand",string="Brand")
    evaporator_equipment_model_id = fields.Char(string="Model")
    evaporator_equipment_serial_number = fields.Char(string="Serial #")
    evaporator_equipment_install_date =  fields.Date(string="Install date",readonly=True,compute="_compute_evaporator_install_date")
    evaporator_equipment_month_install = fields.Selection([('1','January'),('2','February'),('3','March'),('4','April'),('5','May'),('6','June'),('7','July'),('8','August'),('9','September'),('10','October'),('11','November'),('12','December')],string="Month")
    evaporator_equipment_year_install = fields.Selection([('2022','2022'),('2021','2021'),('2020','2020'),('2019','2019'),('2018','2018'),('2017','2017'),('2016','2016'),('2015','2015'),('2014','2014'),('2013','2013'),('2012','2012'),('2011','2011'),('2010','2010'),('2009','2009'),('2008','2008'),('2007','2007'),('2006','2006'),('2005','2005'),('2004','2004'),('2003','2003'),('2002','2002'),('2001','2001'),('2000','2000'),('1999','1999'),('1998','1998'),('1997','1997'),('1996','1996'),('1995','1995'),('1994','1994'),('1993','1993'),('1992','1992'),('1991','1991'),('1990','1990')], string="Year")


    evaporator_component_ids = fields.One2many("pm.evaporator.component","pm_system_id",string="Evaporator Components")

    fancoil_bool = fields.Boolean(string="FanCoil")
    fancoil_component_name = fields.Many2one("preventive_maintenance.component",string="Component Name")
    fancoil_section_id = fields.Many2one("preventive_maintenance.section", string="Component Section")
    fancoil_component_sub_category = fields.Char(related="fancoil_component_name.component_sub_category",string="Component Sub Category")
    fancoil_service_life = fields.Integer(related="fancoil_component_name.service_life",string="Service Life")
    fancoil_equipment_id = fields.Many2one("preventive_maintenance.equipment",string="Equipment")
    fancoil_equipment_brand_id = fields.Many2one("preventive_maintenance.brand",string="Brand")
    fancoil_equipment_model_id = fields.Char(string="Model")
    fancoil_equipment_serial_number = fields.Char(string="Serial #")
    fancoil_equipment_install_date =  fields.Date(string="Install date",readonly=True,compute="_compute_fancoil_install_date")
    fancoil_equipment_month_install = fields.Selection([('1','January'),('2','February'),('3','March'),('4','April'),('5','May'),('6','June'),('7','July'),('8','August'),('9','September'),('10','October'),('11','November'),('12','December')],string="Month")
    fancoil_equipment_year_install = fields.Selection([('2022','2022'),('2021','2021'),('2020','2020'),('2019','2019'),('2018','2018'),('2017','2017'),('2016','2016'),('2015','2015'),('2014','2014'),('2013','2013'),('2012','2012'),('2011','2011'),('2010','2010'),('2009','2009'),('2008','2008'),('2007','2007'),('2006','2006'),('2005','2005'),('2004','2004'),('2003','2003'),('2002','2002'),('2001','2001'),('2000','2000'),('1999','1999'),('1998','1998'),('1997','1997'),('1996','1996'),('1995','1995'),('1994','1994'),('1993','1993'),('1992','1992'),('1991','1991'),('1990','1990')], string="Year")


    fancoil_component_ids = fields.One2many("pm.fancoil.component","pm_system_id",string="Fancoil Components")

    thermostat_bool = fields.Boolean(string="Thermostat")
    thermostat_component_name = fields.Many2one("preventive_maintenance.component",string="Component Name")
    thermostat_section_id = fields.Many2one("preventive_maintenance.section", string="Component Section")
    thermostat_component_sub_category = fields.Char(related="thermostat_component_name.component_sub_category",string="Component Sub Category")
    thermostat_service_life = fields.Integer(related="thermostat_component_name.service_life",string="Service Life")
    thermostat_equipment_id = fields.Many2one("preventive_maintenance.equipment",string="Equipment")
    thermostat_equipment_brand_id = fields.Many2one("preventive_maintenance.brand",string="Brand")
    thermostat_equipment_model_id = fields.Char(string="Model")
    thermostat_equipment_serial_number = fields.Char(string="Serial #")
    thermostat_equipment_install_date =  fields.Date(string="Install date",readonly=True,compute="_compute_thermostat_install_date")
    thermostat_equipment_month_install = fields.Selection([('1','January'),('2','February'),('3','March'),('4','April'),('5','May'),('6','June'),('7','July'),('8','August'),('9','September'),('10','October'),('11','November'),('12','December')],string="Month")
    thermostat_equipment_year_install = fields.Selection([('2022','2022'),('2021','2021'),('2020','2020'),('2019','2019'),('2018','2018'),('2017','2017'),('2016','2016'),('2015','2015'),('2014','2014'),('2013','2013'),('2012','2012'),('2011','2011'),('2010','2010'),('2009','2009'),('2008','2008'),('2007','2007'),('2006','2006'),('2005','2005'),('2004','2004'),('2003','2003'),('2002','2002'),('2001','2001'),('2000','2000'),('1999','1999'),('1998','1998'),('1997','1997'),('1996','1996'),('1995','1995'),('1994','1994'),('1993','1993'),('1992','1992'),('1991','1991'),('1990','1990')], string="Year")


    thermostat_component_ids = fields.One2many("pm.thermostat.component","pm_system_id",string="Thermostat Components")

    airflow_ducting_bool = fields.Boolean(string="Airflow & Ducting")
    airflow_ducting_component_name = fields.Many2one("preventive_maintenance.component",string="Component Name")
    airflow_ducting_section_id = fields.Many2one("preventive_maintenance.section", string="Component Section")
    airflow_ducting_component_sub_category = fields.Char(related="airflow_ducting_component_name.component_sub_category",string="Component Sub Category")
    airflow_ducting_service_life = fields.Integer(related="airflow_ducting_component_name.service_life",string="Service Life")
    airflow_ducting_equipment_id = fields.Many2one("preventive_maintenance.equipment",string="Equipment")
    pm_component_airflow_ids = fields.One2many("pm.component.airflow.record","pm_system_id",string="AirFlow Components")



    blower_bool = fields.Boolean(string="Blower")
    blower_component_name = fields.Many2one("preventive_maintenance.component",string="Component Name")
    blower_section_id = fields.Many2one("preventive_maintenance.section", string="Component Section")
    blower_component_sub_category = fields.Char(related="blower_component_name.component_sub_category",string="Component Sub Category")
    blower_service_life = fields.Integer(related="blower_component_name.service_life",string="Service Life")
    blower_equipment_id = fields.Many2one("preventive_maintenance.equipment",string="Equipment")
    blower_equipment_brand_id = fields.Many2one("preventive_maintenance.brand",string="Brand")
    blower_equipment_model_id = fields.Char(string="Model")
    blower_equipment_serial_number = fields.Char(string="Serial #")
    blower_equipment_install_date =  fields.Date(string="Install date",readonly=True,compute="_compute_blower_install_date")
    blower_equipment_month_install = fields.Selection([('1','January'),('2','February'),('3','March'),('4','April'),('5','May'),('6','June'),('7','July'),('8','August'),('9','September'),('10','October'),('11','November'),('12','December')],string="Month")
    blower_equipment_year_install = fields.Selection([('2022','2022'),('2021','2021'),('2020','2020'),('2019','2019'),('2018','2018'),('2017','2017'),('2016','2016'),('2015','2015'),('2014','2014'),('2013','2013'),('2012','2012'),('2011','2011'),('2010','2010'),('2009','2009'),('2008','2008'),('2007','2007'),('2006','2006'),('2005','2005'),('2004','2004'),('2003','2003'),('2002','2002'),('2001','2001'),('2000','2000'),('1999','1999'),('1998','1998'),('1997','1997'),('1996','1996'),('1995','1995'),('1994','1994'),('1993','1993'),('1992','1992'),('1991','1991'),('1990','1990')], string="Year")

    
    blower_component_ids = fields.One2many("pm.blower.component","pm_system_id",string="Blower Components")

    water_drainage_bool = fields.Boolean(string="Water & Drainage")
    water_drainage_component_name = fields.Many2one("preventive_maintenance.component",string="Component Name")
    water_drainage_section_id = fields.Many2one("preventive_maintenance.section", string="Component Section")
    water_drainage_component_sub_category = fields.Char(related="water_drainage_component_name.component_sub_category",string="Component Sub Category")
    water_drainage_service_life = fields.Integer(related="water_drainage_component_name.service_life",string="Service Life")
    water_drainage_equipment_id = fields.Many2one("preventive_maintenance.equipment",string="Equipment")
    water_drainage_equipment_brand_id = fields.Many2one("preventive_maintenance.brand",string="Brand")
    #water_drainage_equipment_model_id = fields.Many2one("preventive_maintenance.brand.model",string="Model")
    water_drainage_equipment_model_id = fields.Char(string="Model")
    water_drainage_equipment_serial_number = fields.Char(string="Serial #")
    water_drainage_equipment_install_date =  fields.Date(string="Install date",readonly=True,compute="_compute_water_drainage_install_date")
    water_drainage_equipment_month_install = fields.Selection([('1','January'),('2','February'),('3','March'),('4','April'),('5','May'),('6','June'),('7','July'),('8','August'),('9','September'),('10','October'),('11','November'),('12','December')],string="Month")
    water_drainage_equipment_year_install = fields.Selection([('2022','2022'),('2021','2021'),('2020','2020'),('2019','2019'),('2018','2018'),('2017','2017'),('2016','2016'),('2015','2015'),('2014','2014'),('2013','2013'),('2012','2012'),('2011','2011'),('2010','2010'),('2009','2009'),('2008','2008'),('2007','2007'),('2006','2006'),('2005','2005'),('2004','2004'),('2003','2003'),('2002','2002'),('2001','2001'),('2000','2000'),('1999','1999'),('1998','1998'),('1997','1997'),('1996','1996'),('1995','1995'),('1994','1994'),('1993','1993'),('1992','1992'),('1991','1991'),('1990','1990')], string="Year")


    water_drainage_component_ids = fields.One2many("pm.water.drainage.component","pm_system_id",string="Water Drainage Components")

    iaq_bool = fields.Boolean(string="IAQ")
    iaq_component_name = fields.Many2one("preventive_maintenance.component",string="Component Name")
    iaq_section_id = fields.Many2one("preventive_maintenance.section", string="Component Section")
    iaq_component_sub_category = fields.Char(related="iaq_component_name.component_sub_category",string="Component Sub Category")
    iaq_service_life = fields.Integer(related="iaq_component_name.service_life",string="Service Life")
    iaq_equipment_id = fields.Many2one("preventive_maintenance.equipment",string="Equipment")
    iaq_equipment_brand_id = fields.Many2one("preventive_maintenance.brand",string="Brand")
    iaq_equipment_model_id = fields.Char(string="Model")
    iaq_equipment_serial_number = fields.Char(string="Serial #")
    iaq_equipment_install_date =  fields.Date(string="Install date",readonly=True,compute="_compute_iaq_install_date")
    iaq_equipment_month_install = fields.Selection([('1','January'),('2','February'),('3','March'),('4','April'),('5','May'),('6','June'),('7','July'),('8','August'),('9','September'),('10','October'),('11','November'),('12','December')],string="Month")
    iaq_equipment_year_install = fields.Selection([('2022','2022'),('2021','2021'),('2020','2020'),('2019','2019'),('2018','2018'),('2017','2017'),('2016','2016'),('2015','2015'),('2014','2014'),('2013','2013'),('2012','2012'),('2011','2011'),('2010','2010'),('2009','2009'),('2008','2008'),('2007','2007'),('2006','2006'),('2005','2005'),('2004','2004'),('2003','2003'),('2002','2002'),('2001','2001'),('2000','2000'),('1999','1999'),('1998','1998'),('1997','1997'),('1996','1996'),('1995','1995'),('1994','1994'),('1993','1993'),('1992','1992'),('1991','1991'),('1990','1990')], string="Year")



    iaq_component_ids = fields.One2many("pm.iaq.component","pm_system_id",string="IAQ Components")

    #hidden boolean fields
    hid_furnace_bool = fields.Boolean(string="Furnace")
    hid_condenser_bool = fields.Boolean(string="Condenser")
    hid_evaporator_bool = fields.Boolean(string="Evaporator")
    hid_fancoil_bool = fields.Boolean(string="FanCoil")
    hid_thermostat_bool = fields.Boolean(string="Thermostat")
    hid_airflow_ducting_bool = fields.Boolean(string="Airflow & Ducting")
    hid_blower_bool = fields.Boolean(string="Blower")
    hid_water_drainage_bool = fields.Boolean(string="Water & Drainage")
    hid_iaq_bool = fields.Boolean(string="IAQ")
    
    #Install dates for each equipment

    @api.depends('furnace_equipment_month_install','furnace_equipment_year_install')
    def _compute_furnace_install_date(self):
        for record in self:

            date_value = False

            if record.furnace_equipment_month_install and record.furnace_equipment_year_install:
                date_value = datetime.date(int(record.furnace_equipment_year_install),int(record.furnace_equipment_month_install),1)

            if record['furnace_equipment_install_date'] != date_value:
                record['furnace_equipment_install_date'] = date_value

                for component in record.furnace_component_ids:
                    component['install_date'] = date_value

        return True

    @api.depends('condenser_equipment_month_install','condenser_equipment_year_install')
    def _compute_condenser_install_date(self):
        for record in self:

            date_value = False

            if record.condenser_equipment_month_install and record.condenser_equipment_year_install:
                date_value = datetime.date(int(record.condenser_equipment_year_install),int(record.condenser_equipment_month_install),1)

            if record['condenser_equipment_install_date'] != date_value:
                record['condenser_equipment_install_date'] = date_value

                for component in record.condenser_component_ids:
                    component['install_date'] = date_value

        return True

    @api.depends('evaporator_equipment_month_install','evaporator_equipment_year_install')
    def _compute_evaporator_install_date(self):
        for record in self:

            date_value = False

            if record.evaporator_equipment_month_install and record.evaporator_equipment_year_install:
                date_value = datetime.date(int(record.evaporator_equipment_year_install),int(record.evaporator_equipment_month_install),1)

            if record['evaporator_equipment_install_date'] != date_value:
                record['evaporator_equipment_install_date'] = date_value

                for component in record.evaporator_component_ids:
                    component['install_date'] = date_value

        return True

    @api.depends('fancoil_equipment_month_install','fancoil_equipment_year_install')
    def _compute_fancoil_install_date(self):
        for record in self:

            date_value = False

            if record.fancoil_equipment_month_install and record.fancoil_equipment_year_install:
                date_value = datetime.date(int(record.fancoil_equipment_year_install),int(record.fancoil_equipment_month_install),1)

            if record['fancoil_equipment_install_date'] != date_value:
                record['fancoil_equipment_install_date'] = date_value

                for component in record.fancoil_component_ids:
                    component['install_date'] = date_value

        return True

    @api.depends('thermostat_equipment_month_install','thermostat_equipment_year_install')
    def _compute_thermostat_install_date(self):
        for record in self:

            date_value = False

            if record.thermostat_equipment_month_install and record.thermostat_equipment_year_install:
                date_value = datetime.date(int(record.thermostat_equipment_year_install),int(record.thermostat_equipment_month_install),1)

            if record['thermostat_equipment_install_date'] != date_value:
                record['thermostat_equipment_install_date'] = date_value

                for component in record.thermostat_component_ids:
                    component['install_date'] = date_value

        return True

    @api.depends('blower_equipment_month_install','blower_equipment_year_install')
    def _compute_blower_install_date(self):
        for record in self:

            date_value = False

            if record.blower_equipment_month_install and record.blower_equipment_year_install:
                date_value = datetime.date(int(record.blower_equipment_year_install),int(record.blower_equipment_month_install),1)

            if record['blower_equipment_install_date'] != date_value:
                record['blower_equipment_install_date'] = date_value

                for component in record.blower_component_ids:
                    component['install_date'] = date_value

        return True

    @api.depends('water_drainage_equipment_month_install','water_drainage_equipment_year_install')
    def _compute_water_drainage_install_date(self):
        for record in self:

            date_value = False

            if record.water_drainage_equipment_month_install and record.water_drainage_equipment_year_install:
                date_value = datetime.date(int(record.water_drainage_equipment_year_install),int(record.water_drainage_equipment_month_install),1)

            if record['water_drainage_equipment_install_date'] != date_value:
                record['water_drainage_equipment_install_date'] = date_value

                for component in record.water_drainage_component_ids:
                    component['install_date'] = date_value

        return True

    @api.depends('iaq_equipment_month_install','iaq_equipment_year_install')
    def _compute_iaq_install_date(self):
        for record in self:

            date_value = False

            if record.iaq_equipment_month_install and record.iaq_equipment_year_install:
                date_value = datetime.date(int(record.iaq_equipment_year_install),int(record.iaq_equipment_month_install),1)

            if record['iaq_equipment_install_date'] != date_value:
                record['iaq_equipment_install_date'] = date_value

                for component in record.iaq_component_ids:
                    component['install_date'] = date_value

        return True
    
    @api.onchange(*equipment_list_id)
    def cascade_install_date_component(self):
        for record in self:
            field_trigger = False
            for field in record.equipment_list_id:
                if record[field] != record._origin[field]:
                    field_trigger = field
                    record._origin[field] = record[field]
                    break
            if field_trigger:
                field = field_trigger.replace("_equipment_id","")
                for component in record['%s_component_ids' % field]:
                    component["install_date"] = record['%s_equipment_install_date' % field]
#             raise UserError(field_trigger)
    
    @api.onchange(*equipment_list_bool)
    def cascade_install_date(self):
        for record in self:
            for field_trigger in record.equipment_list_bool:
                field = field_trigger.replace("_bool","")
                if record[field_trigger]:
                    if not record["%s_equipment_month_install" % field]:
                        record["%s_equipment_month_install" % field] = record.month_install
                    if not record["%s_equipment_year_install" % field]:
                        record["%s_equipment_year_install" % field] = record.year_install
                else:
                    record["%s_equipment_month_install" % field] = False
                    record["%s_equipment_year_install" % field] = False
                    record["%s_equipment_year_install" % field] = False
    
    @api.onchange(*list_brand)
    def cascade_equipment(self):
        for record in self:
            list_without_system = record.list_brand[1:]
            field_trigger = False
            for field in record.list_brand:
                if record[field] != record._origin[field]:
                    field_trigger = field
                    record._origin[field] = record[field]
                    break
            if field_trigger:
                if field_trigger == 'brand':
                    for equipment_brand in list_without_system:
                          if record["%s_bool" % equipment_brand.replace('_equipment_brand_id','')] == True:
                            record[equipment_brand] = record['brand']
                            self.cascade_component(equipment_brand)
                else:
                    record[field_trigger] = record[field_trigger]
                    self.cascade_component(field_trigger)
    
    def cascade_component(self, equipment):
         for record in self:  
                equipment_name = equipment.replace('_equipment_brand_id','')
                for component in record["%s_component_ids" % equipment_name]:
                    component["brand_id"] = record[equipment]
                   
    @api.depends('month_install','year_install')
    def _compute_install_date(self):
        for record in self:

            date_value = False

            if record.month_install and record.year_install:
                date_value = datetime.date(int(record.year_install),int(record.month_install),1)

            record['first_install'] = date_value
            
            for equipment in record.equipment_list:  
                if record["%s_bool" % equipment] == True:
                    if record["%s_equipment_install_date" % equipment] == False:
                        record["%s_equipment_install_date" % equipment] = record['first_install']
                        record["%s_equipment_month_install" % equipment] = record.month_install
                        record["%s_equipment_year_install" % equipment] = record.year_install

        return True
    
    @api.depends('month_install','year_install')
    def _compute_brand(self):
        for record in self:

            date_value = False

            if record.month_install and record.year_install:
                date_value = datetime.date(int(record.year_install),int(record.month_install),1)

            record['first_install'] = date_value
            
            for equipment in record.equipment_list:  
                if record["%s_bool" % equipment] == True:
                    if record["%s_equipment_install_date" % equipment] == False:
                        record["%s_equipment_install_date" % equipment] = record['first_install']
                        record["%s_equipment_month_install" % equipment] = record.month_install
                        record["%s_equipment_year_install" % equipment] = record.year_install

        return True
    
    # Verify if a last_test date is on a equipment component, then make readonly
    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        system = super(System, self).fields_view_get(
                view_id=view_id, view_type=view_type, toolbar=toolbar,
                submenu=submenu,
            )
        if view_type == 'form':
            pm_systems = self.env['preventive_maintenance.system'].search([])
            for pm_system in pm_systems:
                for equipment in self.equipment_list:
                    fields_readonly = ['%s_bool' % equipment,'%s_equipment_id' % equipment,'%s_equipment_brand_id' % equipment,'%s_equipment_model_id' % equipment,'%s_equipment_serial_number' % equipment,'%s_equipment_install_date' % equipment,'%s_equipment_month_install' % equipment,'%s_equipment_year_install' % equipment]
                    has_last_test_date = False
                    components = pm_system['%s_component_ids' % equipment]

                    for component in components:
                        if component.last_test != False:
                            has_last_test_date = True
                            break

                    doc = etree.XML(system['arch'])
                    for field_readonly in fields_readonly:
                        for node in doc.xpath("//field[@name='%s']" % field_readonly):
                            node.set("readonly", "%s" % ("1" if has_last_test_date else "0"))
                            modifiers = json.loads(node.get("modifiers"))
                            modifiers['readonly'] = has_last_test_date
                            node.set("modifiers", json.dumps(modifiers))
                            system['arch'] = etree.tostring(doc)
        return system

    @api.onchange('first_install')
    def _compute_system_age(self):
        for record in self:
            age = False

            if record.first_install:
                #Compute how many months since install
                today = datetime.datetime.today()

                age = ((today.year-record.first_install.year)*12 + (today.month-record.first_install.month))/12
                
            record['system_age'] = age
#         return True

    ##
    #
    # Airflow & Ducting fields & calculation
    #
    ##

    airflow_ducting_component_ids = fields.One2many("pm.airflow.ducting.component","pm_system_id",string="Airflow & Ducting Components")

    directional_flow = fields.Selection([('horizontal_ltr','Horizontal - Left to Right'),('horizontal_rtl','Horizontal - Right to Left'),('vertical_downflow','Vertical - Downflow'),('vertical_upflow','Vertical - Upflow')], string="Equipment direction")
    airflow_supply_component_ids = fields.One2many("pm.component.airflow.record","pm_system_id",string="Airflow Supply Components")

    airflow = fields.Char(string="Airflow", compute="_compute_airflow", stored=False)

    aeroseal_completed = fields.Boolean(string="Aeroseal completed ?")
    aeroseal_date = fields.Date(string="Aeroseal date")

        

    def _compute_airflow(self):
        string = "Airflow OK"
        total_supply = 0.0
        total_return = 0.0
        total_filter_coeff = 0.0
        type_with_issue = " - "
        min_cfm = 0.0

        if self.tons != False:
            min_cfm = 400*float(self.tons)

            ## Supply 
            # for supply_comp in self.pm_component_airflow_ids.filtered(lambda c: c.airflow_component_type.supply_or_return == "supply"):
                
            flex_supp_cfm = 0.0
            for flex_duct_comp in self.pm_component_airflow_ids.filtered(lambda f: f.airflow_component.airflow_component_type.name =='Flex Duct' and f.airflow_component.airflow_component_type.supply_or_return in ["supply","both"]):
                flex_supp_cfm += flex_duct_comp.cfm

            if flex_supp_cfm < min_cfm:
                string = "Airflow NOK"
                type_with_issue += "Supply Flex Duct : "+str(flex_supp_cfm)+"; expected min :"+str(min_cfm)+"\n"


            hard_supp_cfm = 0.0
            for hard_duct_comp in self.pm_component_airflow_ids.filtered(lambda f: f.airflow_component.airflow_component_type.name =='Hard Duct' and f.airflow_component.airflow_component_type.supply_or_return in ["supply","both"]):
                hard_supp_cfm += hard_duct_comp.cfm

            if hard_supp_cfm < min_cfm:
                string = "Airflow NOK"
                type_with_issue += "Supply Hard Duct : "+str(hard_supp_cfm)+"; expected min :"+str(min_cfm)+"\n"
                

            plenum_supp_cfm = 0.0
            for plenum_duct_comp in self.pm_component_airflow_ids.filtered(lambda f: f.airflow_component.airflow_component_type.name =='Plenums' and f.airflow_component.airflow_component_type.supply_or_return in ["supply","both"]):
                plenum_supp_cfm += plenum_duct_comp.cfm

            if plenum_supp_cfm < min_cfm:
                string = "Airflow NOK"
                type_with_issue += "Supply Plenums : "+str(plenum_supp_cfm)+"; expected min :"+str(min_cfm)+"\n"

            total_supply = flex_supp_cfm+hard_supp_cfm+plenum_supp_cfm


            ## Returns
            # for return_comp in self.pm_component_airflow_ids.filtered(lambda c: c.airflow_component_type.supply_or_return == "return"):
                
            #Air filter coeff
            for air_filter in self.pm_component_airflow_ids.filtered(lambda f: f.airflow_component.airflow_component_type.name =='Air Filters' and f.airflow_component.airflow_component_type.supply_or_return in ["return","both"]):
                total_filter_coeff += air_filter.filter_coefficient
            intake_cfm = 0.0
            for intake_comp in self.pm_component_airflow_ids.filtered(lambda f: f.airflow_component.airflow_component_type.name =='Intakes' and f.airflow_component.airflow_component_type.supply_or_return in ["return","both"]):
                intake_cfm += intake_comp.cfm

            intake_cfm = intake_cfm*total_filter_coeff
            if intake_cfm < min_cfm:
                string = "Airflow NOK"
                type_with_issue += "Return Intakes : "+str(intake_cfm)+"; expected min :"+str(min_cfm)+"\n"

            flex_cfm = 0.0
            for flex_duct_comp in self.pm_component_airflow_ids.filtered(lambda f: f.airflow_component.airflow_component_type.name =='Flex Duct' and f.airflow_component.airflow_component_type.supply_or_return in ["return","both"]):
                flex_cfm += flex_duct_comp.cfm

            flex_cfm = flex_cfm*total_filter_coeff
            if flex_cfm < min_cfm:
                string = "Airflow NOK"
                type_with_issue += "Return Flex Duct : "+str(flex_cfm)+"; expected min :"+str(min_cfm)+"\n"


            hard_cfm = 0.0
            for hard_duct_comp in self.pm_component_airflow_ids.filtered(lambda f: f.airflow_component.airflow_component_type.name =='Hard Duct' and f.airflow_component.airflow_component_type.supply_or_return in ["return","both"]):
                hard_cfm += hard_duct_comp.cfm

            hard_cfm = hard_cfm*total_filter_coeff
            if hard_cfm < min_cfm:
                string = "Airflow NOK"
                type_with_issue += "Return Hard Duct : "+str(hard_cfm)+"; expected min :"+str(min_cfm)+"\n"

            plenum_cfm = 0.0
            for plenum_duct_comp in self.pm_component_airflow_ids.filtered(lambda f: f.airflow_component.airflow_component_type.name =='Plenums' and f.airflow_component.airflow_component_type.supply_or_return in ["return","both"]):
                plenum_cfm += plenum_duct_comp.cfm

            plenum_cfm = plenum_cfm*total_filter_coeff
            if plenum_cfm < min_cfm:
                string = "Airflow NOK"
                type_with_issue += "Return Plenums : "+str(plenum_cfm)+"; expected min :"+str(min_cfm)+"\n"

            total_return = flex_cfm+hard_cfm+plenum_cfm+intake_cfm

            self.airflow = string+type_with_issue+ ("Total Supply : %s / Total return : %s / Expected result : %s" % (total_supply,total_return,min_cfm))
        else :
            self.airflow = "Tonnage not defined"
    
        return True
        
    def _compute_system_health(self):

        for sys in self:
            sys.health = "good"

            component_list = []
            component_list.extend(sys.furnace_component_ids)
            component_list.extend(sys.condenser_component_ids)
            component_list.extend(sys.evaporator_component_ids)
            component_list.extend(sys.fancoil_component_ids)
            component_list.extend(sys.thermostat_component_ids)
            component_list.extend(sys.airflow_ducting_component_ids)
            component_list.extend(sys.blower_component_ids)
            component_list.extend(sys.water_drainage_component_ids)
            component_list.extend(sys.iaq_component_ids)

            for component in component_list:
                if component.component_state == 'warning' and sys.health != 'error':
                    sys.health = 'warning'
                elif component.component_state == 'error':
                    sys.health = 'error'



    @api.model
    def default_get(self, fields):
        res = super(System, self).default_get(fields)
        pm_section = self.env['preventive_maintenance.section']
        pm_component = self.env['preventive_maintenance.component']
        furnace_component_name = False
        furnace_section_id = pm_section.search([('name','=','Furnace')], limit=1).id or False
        if furnace_section_id:
            furnace_component_name = pm_component.search([('section_id','=',furnace_section_id)], limit=1).id
        condenser_component_name = False
        condenser_section_id = pm_section.search([('name','=','Condenser')], limit=1).id or False
        if condenser_section_id:
            condenser_component_name = pm_component.search([('section_id','=',condenser_section_id)], limit=1).id
        evaporator_component_name = False
        evaporator_section_id = pm_section.search([('name','=','Evaporator')], limit=1).id or False
        if evaporator_section_id:
            evaporator_component_name = pm_component.search([('section_id','=',evaporator_section_id)], limit=1).id
        fancoil_component_name = False
        fancoil_section_id = pm_section.search([('name','=','Fancoil')], limit=1).id or False
        if fancoil_section_id:
            fancoil_component_name = pm_component.search([('section_id','=',fancoil_section_id)], limit=1).id
        thermostat_component_name = False
        thermostat_section_id = pm_section.search([('name','=','Thermostat')], limit=1).id or False
        if thermostat_section_id:
            thermostat_component_name = pm_component.search([('section_id','=',thermostat_section_id)], limit=1).id
        airflow_ducting_component_name = False
        airflow_ducting_section_id = pm_section.search([('name','=','Airflow & Ducting')], limit=1).id or False
        if airflow_ducting_section_id:
            airflow_ducting_component_name = pm_component.search([('section_id','=',airflow_ducting_section_id)], limit=1).id
        blower_component_name = False
        blower_section_id = pm_section.search([('name','=','Blower')], limit=1).id or False
        if blower_section_id:
            blower_component_name = pm_component.search([('section_id','=',blower_section_id)], limit=1).id
        water_drainage_component_name = False
        water_drainage_section_id = pm_section.search([('name','=','Water & Drainage')], limit=1).id or False
        if water_drainage_section_id:
            water_drainage_component_name = pm_component.search([('section_id','=',water_drainage_section_id)], limit=1).id
        iaq_component_name = False
        iaq_section_id = pm_section.search([('name','=','IAQ')], limit=1).id or False
        if iaq_section_id:
            iaq_component_name = pm_component.search([('section_id','=',iaq_section_id)], limit=1).id
        res.update({
                'furnace_section_id' : furnace_section_id,
                'furnace_component_name' : furnace_component_name or False,
                'condenser_section_id' : condenser_section_id,
                'condenser_component_name' : condenser_component_name or False,
                'fancoil_section_id' : fancoil_section_id,
                'fancoil_component_name' : fancoil_component_name or False,
                'evaporator_section_id': evaporator_section_id,
                'fancoil_component_name': evaporator_component_name or False,
                'thermostat_section_id': thermostat_section_id,
                'thermostat_component_name': thermostat_component_name or False,
                'airflow_ducting_section_id': airflow_ducting_section_id,
                'airflow_ducting_component_name': airflow_ducting_component_name or False,
                'blower_section_id': blower_section_id,
                'blower_component_name': blower_component_name or False,
                'water_drainage_section_id': water_drainage_section_id,
                'water_drainage_component_name': water_drainage_component_name or False,
                'iaq_section_id': iaq_section_id,
                'iaq_component_name': iaq_component_name or False,
            })
        return res

    @api.onchange('furnace_bool')
    def _onchange_furnace_bool(self):
        furnace_component_name = False
        furnace_section_id = self.env['preventive_maintenance.section'].search([('name','=','Furnace')], limit=1).id or False
        res = {}
        res['domain'] = {'furnace_section_id': [('id','=',furnace_section_id)] or False, 'furnace_equipment_id': [('section_id','=',furnace_section_id)]} #'furnace_component_name': [('id', 'in', component_list)],
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
        self.write({'furnace_component_ids': [(3,exist_comp.id) for exist_comp in self.furnace_component_ids]})
        new_components = []
        if component_ids:
            for new_comp in self.env['preventive_maintenance.component'].browse(component_ids):
                new_components.append({'furnace_component_name': new_comp.id, 'furnace_section_id': new_comp.section_id.id, 'pm_system_id': self.id})
            self.write({'furnace_component_ids': [(0,0,new_cmp) for new_cmp in new_components]})
        res = {}
        res['domain'] = {'furnace_component_name': [('id', 'in', component_ids)]}
        return res

    @api.onchange('condenser_bool')
    def _onchange_condenser_bool(self):
        condenser_component_name = False
        condenser_section_id = self.env['preventive_maintenance.section'].search([('name','=','Condenser')], limit=1).id or False
        res = {}
        res['domain'] = {'condenser_section_id': [('id','=',condenser_section_id)] or False, 'condenser_equipment_id': [('section_id','=',condenser_section_id)]} #'condenser_component_name': [('id', 'in', component_list)],
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
        self.write({'condenser_component_ids': [(3,exist_comp.id) for exist_comp in self.condenser_component_ids]})
        new_components = []
        if component_ids:
            for new_comp in self.env['preventive_maintenance.component'].browse(component_ids):
                new_components.append({'condenser_component_name': new_comp.id, 'condenser_section_id': new_comp.section_id.id, 'pm_system_id': self.id})
            self.write({'condenser_component_ids': [(0,0,new_cmp) for new_cmp in new_components]})
        res = {}
        res['domain'] = {'condenser_component_name': [('id', 'in', component_ids)]}
        return res

    @api.onchange('evaporator_bool')
    def _onchange_evaporator_bool(self):
        evaporator_component_name = False
        evaporator_section_id = self.env['preventive_maintenance.section'].search([('name','=','Evaporator')], limit=1).id or False
        res = {}
        res['domain'] = {'evaporator_section_id': [('id','=',evaporator_section_id)] or False, 'evaporator_equipment_id': [('section_id','=',evaporator_section_id)]} #'evaporator_component_name': [('id', 'in', component_list)],
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
        self.write({'evaporator_component_ids': [(3,exist_comp.id) for exist_comp in self.evaporator_component_ids]})
        new_components = []
        if component_ids:
            for new_comp in self.env['preventive_maintenance.component'].browse(component_ids):
                new_components.append({'evaporator_component_name': new_comp.id, 'evaporator_section_id': new_comp.section_id.id, 'pm_system_id': self.id})
            self.write({'evaporator_component_ids': [(0,0,new_cmp) for new_cmp in new_components]})
        res = {}
        res['domain'] = {'evaporator_component_name': [('id', 'in', component_ids)]}
        return res

    @api.onchange('fancoil_bool')
    def _onchange_fancoil_bool(self):
        fancoil_component_name = False
        fancoil_section_id = self.env['preventive_maintenance.section'].search([('name','=','Fancoil')], limit=1).id or False
        res = {}
        res['domain'] = {'fancoil_section_id': [('id','=',fancoil_section_id)] or False, 'fancoil_equipment_id': [('section_id','=',fancoil_section_id)]} #'fancoil_component_name': [('id', 'in', component_list)],
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
        self.write({'fancoil_component_ids': [(3,exist_comp.id) for exist_comp in self.fancoil_component_ids]})
        new_components = []
        if component_ids:
            for new_comp in self.env['preventive_maintenance.component'].browse(component_ids):
                new_components.append({'fancoil_component_name': new_comp.id, 'fancoil_section_id': new_comp.section_id.id, 'pm_system_id': self.id})
            self.write({'fancoil_component_ids': [(0,0,new_cmp) for new_cmp in new_components]})
        res = {}
        res['domain'] = {'fancoil_component_name': [('id', 'in', component_ids)]}
        return res

    @api.onchange('thermostat_bool')
    def _onchange_thermostat_bool(self):
        thermostat_component_name = False
        thermostat_section_id = self.env['preventive_maintenance.section'].search([('name','=','Thermostat')], limit=1).id or False
        res = {}
        res['domain'] = {'thermostat_section_id': [('id','=',thermostat_section_id)] or False, 'thermostat_equipment_id': [('section_id','=',thermostat_section_id)]}#'thermostat_component_name': [('id', 'in', component_list)],
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
        self.write({'thermostat_component_ids': [(3,exist_comp.id) for exist_comp in self.thermostat_component_ids]})
        new_components = []
        if component_ids:
            for new_comp in self.env['preventive_maintenance.component'].browse(component_ids):
                new_components.append({'thermostat_component_name': new_comp.id, 'thermostat_section_id': new_comp.section_id.id, 'pm_system_id': self.id})
            self.write({'thermostat_component_ids': [(0,0,new_cmp) for new_cmp in new_components]})
        res = {}
        res['domain'] = {'thermostat_component_name': [('id', 'in', component_ids)]}
        return res

    def add_supply(self):
        view_id = self.env['ir.model.data'].xmlid_to_res_id('preventive_maintenance.pm_add_supply_airflow_component_view_form')
        return {
            'type': 'ir.actions.act_window',
            'name': _("Add Supply"),
            'view_mode': 'form',
            'res_model': 'pm.component.airflow.record',
            'views': [[view_id, 'form']],
            'target': 'new',
            'context': {
                'default_pm_system_id': self.id,
                }
            }

    def add_return(self):
        view_id = self.env['ir.model.data'].xmlid_to_res_id('preventive_maintenance.pm_add_return_airflow_component_view_form')
        return {
            'type': 'ir.actions.act_window',
            'name': _("Add Return"),
            'view_mode': 'form',
            'res_model': 'pm.component.airflow.record',
            'views': [[view_id, 'form']],
            'target': 'new',
            'context': {
                'default_pm_system_id': self.id,
                }
            }

    @api.onchange('airflow_ducting_bool')
    def _onchange_airflow_ducting_bool(self):
        airflow_ducting_component_name = False
        airflow_ducting_section_id = self.env['preventive_maintenance.section'].search([('name','=','Airflow & Ducting')], limit=1).id or False
        res = {}
        res['domain'] = {'airflow_ducting_section_id': [('id','=',airflow_ducting_section_id)] or False, 'airflow_ducting_equipment_id': [('section_id','=',airflow_ducting_section_id)]} #'airflow_ducting_component_name': [('id', 'in', component_list)],
        return res

    @api.onchange('airflow_ducting_equipment_id')
    def _onchange_airflow_ducting_equipment_id(self):
        airflow_section_id = self.env['preventive_maintenance.section'].search([('name','=','Airflow & Ducting')], limit=1).id or False
        airflow_component_ids = self.env['preventive_maintenance.component'].search([('section_id','=',airflow_section_id)])
        component_ids = []
        for comp_id in airflow_component_ids:
            if self.airflow_ducting_equipment_id.id in comp_id.component_options.ids:
                component_ids.append(comp_id.id)
            elif not comp_id.component_options:
                component_ids.append(comp_id.id)
        self.write({'airflow_ducting_component_ids': [(3,exist_comp.id) for exist_comp in airflow_component_ids]})
        new_components = []
        if component_ids:
            for new_comp in self.env['preventive_maintenance.component'].browse(component_ids):
                new_components.append({'airflow_ducting_component_name': new_comp.id, 'airflow_ducting_section_id': new_comp.section_id.id, 'pm_system_id': self.id})
            self.write({'airflow_ducting_component_ids': [(0,0,new_cmp) for new_cmp in new_components]})
        res = {}
        res['domain'] = {'airflow_ducting_component_name': [('id', 'in', component_ids)]}
        return res


    @api.onchange('blower_bool')
    def _onchange_blower_bool(self):
        blower_component_name = False
        blower_section_id = self.env['preventive_maintenance.section'].search([('name','=','Blower')], limit=1).id or False
        res = {}
        res['domain'] = {'blower_section_id': [('id','=',blower_section_id)] or False, 'blower_equipment_id': [('section_id','=',blower_section_id)]}#'blower_component_name': [('id', 'in', component_list)],
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
        self.write({'blower_component_ids': [(3,exist_comp.id) for exist_comp in self.blower_component_ids]})
        new_components = []
        if component_ids:
            for new_comp in self.env['preventive_maintenance.component'].browse(component_ids):
                new_components.append({'blower_component_name': new_comp.id, 'blower_section_id': new_comp.section_id.id, 'pm_system_id': self.id})
            self.write({'blower_component_ids': [(0,0,new_cmp) for new_cmp in new_components]})
        res = {}
        res['domain'] = {'blower_component_name': [('id', 'in', component_ids)]}
        return res


    @api.onchange('water_drainage_bool')
    def _onchange_water_drainage_bool(self):
        water_drainage_component_name = False
        water_drainage_section_id = self.env['preventive_maintenance.section'].search([('name','=','Water & Drainage')], limit=1).id or False
        res = {}
        res['domain'] = {'water_drainage_section_id': [('id','=',water_drainage_section_id)] or False, 'water_drainage_equipment_id': [('section_id','=',water_drainage_section_id)]}#'water_drainage_component_name': [('id', 'in', component_list)],
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
        self.write({'water_drainage_component_ids': [(3,exist_comp.id) for exist_comp in self.water_drainage_component_ids]})
        new_components = []
        if component_ids:
            for new_comp in self.env['preventive_maintenance.component'].browse(component_ids):
                new_components.append({'water_drainage_component_name': new_comp.id, 'water_drainage_section_id': new_comp.section_id.id, 'pm_system_id': self.id})
            self.write({'water_drainage_component_ids': [(0,0,new_cmp) for new_cmp in new_components]})
        res = {}
        res['domain'] = {'water_drainage_component_name': [('id', 'in', component_ids)]}
        return res

    @api.onchange('iaq_bool')
    def _onchange_iaq_bool(self):
        iaq_component_name = False
        iaq_section_id = self.env['preventive_maintenance.section'].search([('name','=','IAQ')], limit=1).id or False
        res = {}
        res['domain'] = {'iaq_section_id': [('id','=',iaq_section_id)] or False, 'iaq_equipment_id': [('section_id','=',iaq_section_id)]} #'iaq_component_name': [('id', 'in', component_list)],
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
        self.write({'iaq_component_ids': [(3,exist_comp.id) for exist_comp in self.iaq_component_ids]})
        new_components = []
        if component_ids:
            for new_comp in self.env['preventive_maintenance.component'].browse(component_ids):
                new_components.append({'iaq_component_name': new_comp.id, 'iaq_section_id': new_comp.section_id.id, 'pm_system_id': self.id})
            self.write({'iaq_component_ids': [(0,0,new_cmp) for new_cmp in new_components]})
        res = {}
        res['domain'] = {'iaq_component_name': [('id', 'in', component_ids)]}
        return res

    def set_maintenance_boolean(self):
        system_recs = self.search([])
        for rec in system_recs:
            next_service = rec.next_service
            date_21_after = datetime.datetime.today().date() + datetime.timedelta(days=21)
            if next_service and next_service <= date_21_after:
                rec.maintenance_soon_needed = True
            if rec.health == 'warning':
                rec.maintenance_soon_needed = True
            if rec.health == 'error':
                rec.maintenance_needed = True

    @api.onchange('system_type_id')
    def _onchange_system_type_id(self):
        if self.system_type_id.furnace_bool == True:
            self.hid_furnace_bool = True
        else:
            self.hid_furnace_bool = False
        if self.system_type_id.condenser_bool == True:
            self.hid_condenser_bool = True
        else:
            self.hid_condenser_bool = False
        if self.system_type_id.evaporator_bool == True:
            self.hid_evaporator_bool = True
        else:
            self.hid_evaporator_bool = False
        if self.system_type_id.fancoil_bool == True:
            self.hid_fancoil_bool = True
        else:
            self.hid_fancoil_bool = False
        if self.system_type_id.thermostat_bool == True:
            self.hid_thermostat_bool = True
        else:
            self.hid_thermostat_bool = False
        if self.system_type_id.airflow_ducting_bool == True:
            self.hid_airflow_ducting_bool = True
        else:
            self.hid_airflow_ducting_bool = False
        if self.system_type_id.blower_bool == True:
            self.hid_blower_bool = True
        else:
            self.hid_blower_bool = False
        if self.system_type_id.water_drainage_bool == True:
            self.hid_water_drainage_bool = True
        else:
            self.hid_water_drainage_bool = False
        if self.system_type_id.iaq_bool == True:
            self.hid_iaq_bool = True
        else:
            self.hid_iaq_bool = False
