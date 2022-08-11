from odoo import models, fields, api, _

class ProjectTask(models.Model):
    _inherit = "project.task"

    task_job_type = fields.Selection([('fsm','Job'),('aor','AOR'),('repair','Repair')], string='Job type', compute='_compute_task_job_type')


    def _compute_task_job_type(self):
        for record in self:
            if record.is_fsm:
                record['task_job_type'] = 'fsm'
            else:
                record['task_job_type'] = 'aor'
        return True