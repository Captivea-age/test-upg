

from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, ValidationError


class TestRecord(models.Model):

    _name = "preventive_maintenance.test.records"
    _description = "Test records model"

    system_id = fields.Many2one("preventive_maintenance.system", string="System")
    maintenance_id = fields.Many2one("preventive_maintenance.maintenance", string="Maintenance record")
    component_id = fields.Many2one("preventive_maintenance.component", string="Component")
    job_id = fields.Many2one("project.task", string="Job ID")
    date = fields.Date(string="Date")
    test_type = fields.Many2one("preventive_maintenance.test.category",string="Test type")
    test_type_unit = fields.Char(string="Test unit", related='test_type.test_type_id.name', stored=False)
    value = fields.Char(string="Result value")
    result = fields.Selection([('pass','Pass'),('warning','Warning'),('fail','Fail')],string="Result")
    test_id = fields.Integer(string="test_id")

    sleeping = fields.Boolean(string="Sleeping test", default=True)
    snoozed = fields.Boolean(string="Snoozed test", default=False)

    def testPass(self):
        return self.testOpen(result="pass")

    def testWarning(self):
        return self.testOpen(result="warning")

    def testFail(self):
        return self.testOpen(result="fail")

    def testOpen(self,result="pass"):
        if self.test_type.test_type_id.name != "PFW":
            context = {
                'default_test_id': self.id,
                'default_result': result,
                'default_value':self.value,
                'default_sleeping': False,
                'default_test_type_unit': self.test_type_unit,
            }

            return {
                'type': 'ir.actions.act_window',
                'res_model': 'preventive_maintenance.test.records',
                'view': 'view_pm_test_records_simplified_form',
                'views': [[self.env.ref('preventive_maintenance.view_pm_test_records_simplified_form').id,'form']],
                'view_mode':'form',
#                 'res_id':self.id,
                'target': 'new',
                'context':context,
                'domain':{},
            }
        else:
            self['result'] = result

    def saveTestResultAndClose(self):
        test = self.env['preventive_maintenance.test.records'].search([('id', '=', self.test_id)], limit=1)
        test['value'] = self.value
        test['result'] = self.result

#         return {
#             'type': 'ir.actions.act_window_close'
#         }
