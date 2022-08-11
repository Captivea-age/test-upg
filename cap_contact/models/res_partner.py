# -- coding: utf-8 --
from odoo import models, fields, api, _
from datetime import date, datetime, timedelta
import logging
logger = logging.getLogger(__name__)
from odoo.exceptions import UserError, ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    pm_type = fields.Selection([('post_install_pm','Post Install'),('winter_pm','Winter PM'),('summer_pm','Summer PM'),('inspection_pm','Inspection PM'),('certified_pm','Certified Inspection PM')],string="PM Type")
    out_of_sa = fields.Boolean(string='Out of SA', default=False)
    old_location_name = fields.Char(string='Old Location Name')
    location_type_id = fields.Many2one('location.type', string='Location Type', ondelete='set null')
    partner_type = fields.Selection([('person', 'Person'), ('location', 'Location')], string='Record Type')
    contact_list_ids = fields.One2many('contact.location.relationship', 'location_id', string='Contact Lists')
    location_list_ids = fields.One2many('contact.location.relationship', 'contact_id', string='Location Lists')
    st_create_date = fields.Date(string='ST Create date')
    is_vendor = fields.Boolean(string='Vendor', default=False)
    eligible = fields.Boolean(string='1099 Eligible', default=False)
    job_task_history_ids = fields.Boolean(string='z - do not use', default=False)
    
    partner_age = fields.Char(string='Partner age',compute='_compute_partner_age',store=False)
    monstercare_member = fields.Boolean(string='Monstercare member', default="False")

    def _compute_partner_age(self):
        today = datetime.today()
        if self.st_create_date: 
            date = self.st_create_date
            date = datetime.strptime(date.strftime("%m/%d/%Y"), '%m/%d/%Y')
        else:
            date = self.create_date

        self.partner_age = round(((today-date).days)/365,1)
        return True



    #open System creation popup
    def openSystemCreation(self):
        context = {
            'default_location_id':self.id,
            'default_notification_status':'none',
        }

        view_id = self.env.ref('preventive_maintenance.view_pm_system_form').id
        
        return {
            'type' : 'ir.actions.act_window',
            'name' : 'New system',
            'res_model': 'preventive_maintenance.system',
            'views': [[view_id,'form']],
            'view_mode':'form',
            'context':context,
            'target': 'new',
        }

    def openMaintenancePopup(self):
        context = {
            'default_street':self.street,
        }
        view_id = self.env.ref('cap_contract.view_res_partner_maintenance_form').id
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'view_id': view_id,
            'views': [[view_id,'form']],
            'view_mode':'form',
            'res_id':self.id,
            'target': 'new',
            'context':context,
            'domain':{},
        }

    def addToJob(self,job,test_id):
        if not job:
            helpdesk = self.env['helpdesk.ticket'].create({
                'name':'Maintenance for location :'+str(self.name), 
                'partner_id':self.id,   
                'team_id':2,
            })
            helpdesk.action_generate_fsm_task()
            job = self.env['project.task'].search([('helpdesk_ticket_id','=',helpdesk.id)])[0]

        test_id['job_id']=job.id
        return job


    def generateLocationMaintenance(self):
        
        today = date.today()
        job = False

        #Look for systems
        systems = self.env['preventive_maintenance.system'].search([('location_id','=',self.id)]),
        #Looking for tests specific to this inspection type
        tests = self.env['preventive_maintenance.test.category'].search([(self.pm_type,'=',True)])

        #for each system, check if there's a late test
        for system in systems :
            #Initialize
            maintenance_needed = False
            inspection = False
            notification = False

            #Getting all component ids for this system
            component_list = system.furnace_component_ids.furnace_component_name.ids
            component_list.extend(system.condenser_component_ids.condenser_component_name.ids)
            component_list.extend(system.evaporator_component_ids.evaporator_component_name.ids)
            component_list.extend(system.fancoil_component_ids.fancoil_component_name.ids)
            component_list.extend(system.thermostat_component_ids.thermostat_component_name.ids)
            component_list.extend(system.blower_component_ids.blower_component_name.ids)
            component_list.extend(system.water_drainage_component_ids.water_drainage_component_name.ids)
            component_list.extend(system.iaq_component_ids.iaq_component_name.ids)

            for hs_test in tests.filtered(lambda tests: tests.skill_id.level == 'hard') :
                #checks if system component is present
                if (hs_test.component_id.id in component_list):
                    test_interval_months = hs_test.required_interval
                    previous_task_limit = today-timedelta(days=test_interval_months*30)

                    #Gets previous high skill test done with same system id / test type / date under previous_task_limit
                    similar_hs_test = self.env['preventive_maintenance.test.records'].search([('date','>=',previous_task_limit),('test_type','=',hs_test.id),('system_id','=',system.id)])

            for ls_test in tests.filtered(lambda ls:ls.skill_id.level == 'easy'):
                #checks if system component is present
                if (ls_test.component_id.id in component_list):
                    test_interval_months = ls_test.required_interval
                    previous_task_limit = today-timedelta(days=test_interval_months*30)

                    #Looking for similar low skill task
                similar_ls_test = self.env['preventive_maintenance.test.records'].search([('date','>=',previous_task_limit),('test_type','=',ls_test.id),('system_id','=',system.id)])

            #Inspection creation
            if inspection == False:

                notification =  self.env['preventive_maintenance.notification'].create({
                        'name':'Notification for System :'+str(system.name),
                        'location_id':system.location_id.id,
                        'system_id':system.id,
                        'risk_score':system.base_risk_score,
        #               'dashboard_id':record.id,
                })
                inspection = self.env['preventive_maintenance.maintenance'].create({
                        'name':'Automated preventive maintenance inspection : '+self.pm_type,
                        'system_id':system.id,
                        'pm_type':self.pm_type,
                        'date':today,
                        'state':'warning',
                        'notification_id':notification.id,
                })

            #check high skill tests
            #Will need to order by weight : test_weight .sorted(key=lambda r: r.name)
                for hs_test in tests.filtered(lambda tests: tests.skill_id.level == 'hard') :
                    #checks if scrapped and if system component is present
                    if hs_test.component_id.id in component_list:
                        test_interval_months = hs_test.required_interval
                        previous_task_limit = today-timedelta(days=test_interval_months*30)

                        #Gets previous high skill test done with same system id / test type / date under previous_task_limit
                        similar_hs_test = self.env['preventive_maintenance.test.records'].search([('date','>=',previous_task_limit),('test_type','=',hs_test.id),('system_id','=',system.id)])

                        #if HS test not found, creates an inspection and notification
                        #Also tries to check for the LS tests
                        if len(similar_hs_test)==0:
                            #HS Test creation
                            test = self.env['preventive_maintenance.test.records'].create({
                                'system_id':system.id,
                                'maintenance_id':inspection.id,
                                'component_id':hs_test.component_id.id,
                                'date':today,
                                'test_type':hs_test.id,
                            })
                            job = self.addToJob(job,test)


                            #To avoid having to go over easy tests and later tests each time we check a high skill test
                            #We also check if there enough tls time for LS tests
                
                for ls_test in tests.filtered(lambda ls:ls.skill_id.level == 'easy'):
                    #checks if system component is present
                    if (ls_test.component_id.id in component_list):
                        test_interval_months = ls_test.required_interval
                        previous_task_limit = today-timedelta(days=test_interval_months*30)

                        #Looking for similar low skill task
                        similar_ls_test = self.env['preventive_maintenance.test.records'].search([('date','>=',previous_task_limit),('test_type','=',ls_test.id),('system_id','=',system.id)])

                        if len(similar_ls_test)==0:
                            #Test creation
                            test = self.env['preventive_maintenance.test.records'].create({
                                'system_id':system.id,
                                'maintenance_id':inspection.id,
                                'component_id':ls_test.component_id.id,
                                'date':today,
                                'test_type':ls_test.id,
                            })
                            job = self.addToJob(job,test)

                    #Now adding the later tests that will have to be done (those not late, that will come in ~6months)
                    for ls_future_test in tests.filtered(lambda ls:ls.skill_id.level == 'easy'):
                        #checks if system component is present
                        if ls_future_test.component_id.id in component_list:
                            # required interval + 6months
                            test_interval_months = ls_future_test.required_interval+6
                            future_limit = today-timedelta(days=test_interval_months*30)

                            #Looking for similar low skill task
                            similar_ls_future_test = self.env['preventive_maintenance.test.records'].search([('date','>=',future_limit),('test_type','=',ls_future_test.id),('system_id','=',system.id)])

                            if len(similar_ls_future_test)==0:
                                #Test creation
                                test = self.env['preventive_maintenance.test.records'].create({
                                    'system_id':system.id,
                                    'maintenance_id':inspection.id,
                                    'component_id':ls_future_test.component_id.id,
                                    'date':today,
                                    'test_type':ls_future_test.id,
                                })
                                job = self.addToJob(job,test)


                    #Adding the future high skill tests
                    #At this point, we've done all LS tests and all HS tests + the Future LS tests
                    # "if skip==True" ensures that at least 1 HS test was late and triggered the inspection
                    
                    for hs_future_test in tests.filtered(lambda tests: tests.skill_id.level == 'hard'):
                        #checks if system component is present
                        if hs_future_test.component_id.id in component_list:
                            # required interval + 6months
                            test_interval_months = hs_future_test.required_interval+6
                            future_limit = today-timedelta(days=test_interval_months*30)

                            similar_hs_future_test = self.env['preventive_maintenance.test.records'].search([('date','>=',future_limit),('test_type','=',hs_future_test.id),('system_id','=',system.id)])

                            if len(similar_hs_future_test)==0:
                                #Test creation
                                test = self.env['preventive_maintenance.test.records'].create({
                                    'system_id':system.id,
                                    'maintenance_id':inspection.id,
                                    'component_id':hs_future_test.component_id.id,
                                    'date':today,
                                    'test_type':hs_future_test.id,
                                })
                                job = self.addToJob(job,test)

            # notification.write({
            #   'inspection_time_needed':((high_skill_time_needed+low_skill_time_needed)/60),
            #   'high_skill_time_needed':high_skill_time_needed/60,
            #   'low_skill_time_needed':low_skill_time_needed/60,
            #   'risk_score':risk_score*system.base_risk_score,
            # })
            system.write({
                'notification_status':'pending',
                'health':'error',
            })
            return True
