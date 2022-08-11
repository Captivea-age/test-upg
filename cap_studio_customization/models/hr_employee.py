# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class HREmployee(models.Model):
    _inherit = 'hr.employee'
    
    team_color = fields.Many2one('team.color', string='Team Color', ondelete='set null')
    x_factor_value = fields.Float(compute='_compute_x_factor_value', string='X Factor Value')
    yearly_goal = fields.Integer(string='Yearly Goal')

    @api.depends('__last_update')
    def _compute_x_factor_value(self):
        for record in self:
            today = datetime.datetime.now()
            one_month_ago = today-datetime.timedelta(30)
            record['x_factor_value'] = 0
            xfactor_count = 0
            xfactor_denominator = 0
            xfactor_numerator = 0

            xfactors = self.env['x_factor_journal_id'].search([('user_id','=',record['user_id'].id)])
            if xfactors:
                for xfactor in xfactors:
                    if xfactor['create_date'] >= one_month_ago:
                        xfactor_count += 1
                        xfactor_denominator += xfactor['maximum_value_from_this_category_1']
                        xfactor_numerator += xfactor['points_attributed']
             
                if xfactor_count != 0:
                  record['x_factor_value'] = xfactor_numerator/xfactor_denominator
                else:
                  record['x_factor_value'] = 0
