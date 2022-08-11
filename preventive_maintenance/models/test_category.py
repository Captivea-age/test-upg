

from odoo import models, fields, api, _


class TestCategory(models.Model):

    _name = "preventive_maintenance.test.category"
    _description = "Test category model"

    name = fields.Char(string="Test name")
    section_id = fields.Many2one("preventive_maintenance.section", string="Section")
    component_id = fields.Many2one("preventive_maintenance.component", string="Component")
    test_type_id = fields.Many2one("preventive_maintenance.test", string="Test Type")

    test_list_ids = fields.Many2many("pm.test.list", string='Test list')

    post_install_pm = fields.Boolean(string="Post Install PM")
    first_test = fields.Integer(string="First Test interval")
    required_interval = fields.Integer(string="Required maintenance interval")
    skill_id = fields.Many2one("preventive_maintenance.skill",string="Skill level")
    margin = fields.Selection([('low','Low'),('medium','Medium'),('high','High')],string="Margin")
    time_needed = fields.Integer(string="Time needed")
    winter_pm = fields.Boolean(string="Winter PM")
    summer_pm = fields.Boolean(string="Summer PM")
    inspection_pm = fields.Boolean(string="Inspection PM")
    certified_pm = fields.Boolean(string="Certified Inspection PM")
    test_weight = fields.Float(string="Test Weight percentage")

    def testCreation(self,system_id=False,test_list=False, test_ids=False,job_id=False):
        created_tests_list = []
        VARIABLETOSTORESYSTEMCOMPONENTS = True
        test_full_list = self.env['preventive_maintenance.test.category'].search([])

            # TBD Create all tests


        #Create all tests for a specific list of tests categories required
        if test_ids :
            for test_category in test_ids :
                test = self.env['preventive_maintenance.test.records'].create({
                    'system_id':system_id,
                    'component_id':test_category.component_id.id,
                    'test_type':test_category.id,
                    'job_id':job_id,
                    'sleeping':False,
                    })
                created_tests_list.append(test)

        #Create all tests for a specific list of tests
        elif test_list:
            #Get all tests from list 
            for test_to_generate in test_full_list:
                if test_list in test_to_generate.test_list_ids:
                    # If system, get all components related tests
                    #if test_to_generate.component_id in VARIABLETOSTORESYSTEMCOMPONENTS:

                        test = self.env['preventive_maintenance.test.records'].create({
                        'system_id':system_id.id,
                        'component_id':test_to_generate.component_id.id,
                        'test_type':test_to_generate.id,
                        'job_id':job_id.id,
                        'sleeping':False,
                        })
                
                        created_tests_list.append(test)
