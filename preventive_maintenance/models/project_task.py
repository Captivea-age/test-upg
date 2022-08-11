from odoo import models, fields, api, _


class ProjectTask(models.Model):
    _inherit = "project.task"

    inspections_ids = fields.One2many('preventive_maintenance.maintenance','job_id',string="Inspections")
    test_ids = fields.Many2many('preventive_maintenance.test.records','job_id',string="Test records",compute="_compute_test_ids",stored=False)
    test_ids_smartphone = fields.Many2many('preventive_maintenance.test.records','job_id',string="Test records",compute="_compute_test_ids",stored=False)
    sleeping_test_ids = fields.Many2many('preventive_maintenance.test.records','job_id',string="Test records",compute="_compute_sleeping_test_ids",stored=False)
    system_ids = fields.One2many('preventive_maintenance.system',related='partner_id.system_ids')
    system_selection = fields.Many2one('preventive_maintenance.system',string="System selection")
    sleeping_list_invisible = fields.Boolean('Sleeping invisible', stored=False, default=False)

    def openTestListPopup(self):
        context = {
            'default_job_id':self.id,            
            'default_system_id':self.system_selection.id,            
        }
        test = self.env['preventive_maintenance.test.category']
        system_id = self.system_selection.id
        job_id = self.id

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'pm.test.list.popup',
            'view': 'view_pm_test_list_popup_form',
            'views': [(self.env.ref('preventive_maintenance.view_pm_test_list_popup_form').id,'form')],
            'view_mode':'form',
            'target': 'new',
            'context':context,
            'domain':{},
        }
    def openSystemCreation(self):
        context = {
            'default_location_id':self.partner_id.id,
            'default_notification_status':'none',
        }
        
        return {
            'type' : 'ir.actions.act_window',
            'name' : 'New system',
            'res_model': 'preventive_maintenance.system',
            'views': [[self.env.ref('preventive_maintenance.view_pm_system_form').id,'form']],
            'view_mode':'form',
            'view_type':'form',
            'context':context,
            'target': 'new',
        }
    @api.depends('system_selection')
    def _compute_test_ids(self):
        tests_to_display = []
        #Get all tests mandatory for the selected system
        if self.system_selection:
            system_id = self.system_selection.id
            tests_to_display = self.env['preventive_maintenance.test.records'].search([('system_id','=',system_id),('sleeping','=',False),('snoozed','=',False)])

        else:
            system_ids = self.env['preventive_maintenance.system'].search([('location_id','=','partner_id'),('active','=',True)])
            system_id = []
            for system in system_ids :
                system_id.append(system.id)

            tests_to_display = self.env['preventive_maintenance.test.records'].search([('system_id','in',system_id),('sleeping','=',False),('snoozed','=',False)])
            
        self.update({
            'test_ids':[(6, 0, tests_to_display.ids)],
            'test_ids_smartphone':[(6, 0, tests_to_display.ids)],
            })
        return True


    @api.depends('system_selection')
    def _compute_sleeping_test_ids(self):
        tests_to_display = []

        #Get all tests sleeping for the selected system
        if self.system_selection:
            system_id = self.system_selection.id
            tests_to_display = self.env['preventive_maintenance.test.records'].search([('system_id','=',system_id),'|',('sleeping','=',True),('snoozed','=',True),'|',('sleeping','=',False),('snoozed','=',True)])
        
        else:
            system_ids = self.env['preventive_maintenance.system'].search([('location_id','=','partner_id'),('active','=',True)])
            system_id = []
            for system in system_ids :
                system_id.append(system.id)

            tests_to_display = self.env['preventive_maintenance.test.records'].search([('system_id','in',system_id),'|',('sleeping','=',True),('snoozed','=',True),'|',('sleeping','=',False),('snoozed','=',True)])
        
        self.update({
            'sleeping_test_ids':[(6, 0, tests_to_display.ids)],
        })
        return True