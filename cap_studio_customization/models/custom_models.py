# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class Componants(models.Model):
    _name='cap.componant'
    _description = 'Componants'

    name = fields.Char(string='Name')
    sequence = fields.Integer(string='Sequence')
    image = fields.Binary(string='Image')
    active = fields.Boolean(string='Active', default=True)


class Equipment(models.Model):
    _name='cap.equipment'
    _description = 'Equipment'
    _order = 'sequence asc, id asc'

    name = fields.Char(string='Name')
    active = fields.Boolean(string='Active', default=True)
    sequence = fields.Integer(string='Sequence')


class JobType(models.Model):
    _name='job.type'
    _description = 'Job Type'

    name = fields.Char(string='Name')
    active = fields.Boolean(string='Active', default=True)
    department_id = fields.Many2one('cap.department', string='Department', ondelete='set null')
    tags_to_add_ids = fields.Many2many('helpdesk.tag', 'helpdesk_tag_job_type_rel', 'tag_id', 'job_type_id', string='Tags To Add')
    location_types_ids = fields.Many2many('location.type', 'job_type_location_type_rel', 'job_type_id', 'location_type_id', string='Location Types')
    installation_type = fields.Boolean(string='Installation Type')
    time_needed_hours = fields.Float(string='Time needed (hours)')
    description = fields.Text(string='Description')
    sequence = fields.Integer(string='Sequence')
    default_quotation_template = fields.Many2one('sale.order.template', string='Default Quotation Template', ondelete='set null')


class LocationType(models.Model):
    _name='location.type'
    _description = 'Location Type'

    name = fields.Char(string='Name')
    active = fields.Boolean(string='Active', default=True)
    sequence = fields.Integer(string='Sequence')


class PointsCategories(models.Model):
    _name='points.categories'
    _description = 'Points Categories'

    name = fields.Char(string='Name')
    active = fields.Boolean(string='Active', default=True)
    monitored_field_name_id = fields.Many2one('ir.model.fields', string='Monitored Field Name', ondelete='set null')
    image = fields.Binary(string='Image')
    model_id = fields.Many2one('ir.model', string='Model Name', ondelete='set null')
    maximum_points = fields.Integer(string='Maximum Points')
    additional_parameters = fields.Text(string='Additional Parameters')
    sequence = fields.Integer(string='Sequence')
    monitoring_value = fields.Char(string='Monitoring Value')
    notes = fields.Text(string='Description')
    monitoring_type = fields.Selection([('Value change', 'Value change'), ('Character count', 'Character count'), ('State change', 'State change')],string='Monitoring Type')
    operator = fields.Selection([('==', '=='), ('!=', '!='), ('&gt;', '&gt;'), ('&lt;', '&lt;'), ('&gt;=', '&gt;='), ('&lt;=', '&lt;=')],string='Operator')


class Popup(models.Model):
    _name='cap.popup'
    _description = 'Popup'

    name = fields.Char(string='Name')
    active = fields.Boolean(string='Active', default=True)
    yearly_goal = fields.Html(string='Yearly Goal', store=True)
    xfactor_recap = fields.Html(compute='_compute_xfactor_recap', string='XFactor Recap')
    points_recap = fields.Html(compute='_compute_points_recap', string='Points Recap')
    yearly_target = fields.Html(compute='_compute_yearly_target', string='Yearly Target')
    task_id = fields.Many2one('project.task', string='Task ID', ondelete='set null')
    sequence = fields.Integer(string='Sequence')
    user_id = fields.Many2one('res.users', string='Responsible', ondelete='set null')

    @api.depends('create_date')
    def _compute_yearly_target(self):
        for record in self:
            goal = record.env['gamification.goal'].search([('user_id','=',record['task_id']['user_id'].id),('definition_id','=',5),('state','=','inprogress')])
            goal.update_goal()
            
            difference = goal['current']-goal['target_goal']
            begining = '<h2>Yearly target recap :</h2><br/>'
            header = '<table class="table table-hover table-striped"><tr><th colspan="2">Points summary:</th></tr>'
            body=('<tr><td>Target point: </td><td>'+str(goal['target_goal'])+'</td></tr>'+
                    '<tr><td>Actual: </td><td>'+str(round(goal['current']))+'</td></tr>'+
                    '<tr><td>Difference: </td><td>'+str(round(difference))+'</td></tr>'
                )
            record['yearly_target'] = begining+header+body

    @api.depends('create_date')
    def _compute_points_recap(self):
        for record in self:
            points = record.env['points'].search([('user_id','=',record['task_id']['user_id'].id),('task_id','=',record['task_id'].id)])

            total_value=0
            xfactor = 0
            total_max_points = 0
            beginning = ('<h1>Congratulations '+record['task_id']['user_id']['display_name']+' ! </h1><br/>'+
                        'Thanks to your hard work, you got those points :<br/>')
            header = '<table class="table table-hover table-striped"><tr><th>Points category</th><th>Points attributed</th><th>Category value</th></tr>'

            body = ''
            if len(points)>0:
                for point in points:
                    line = '<tr><td>'+str(point['point_category']['display_name'])+'</td><td>'+str(round(point['points_after_xfactor'],2))+'</td><td>'+str(point['maximum_value_from_this_category'])+'</td></tr>'
                    xfactor = point['x_factor_value_at_this_moment']
                    total_value = total_value+point['points_after_xfactor']
                    total_max_points = total_max_points+point['maximum_value_from_this_category']

                    body = body+line
            
            footer = '<tr><td><b>Total</b></td><td>'+str(round(total_value,2))+'</td><td>'+str(total_max_points)+'</td></tr></table><br/><br/><br/>'

            xfactor_message = 'You had an xfactor of '+str(round(xfactor*100))+'% <br/>'

            if xfactor < 1 :
                xfactor_message= xfactor_message+'You could have earned '+str(total_max_points)+' points, try to raise your Xfactor<br/>'
            else:
                xfactor_message= xfactor_message+'Great job ! Your Xfactor is higher than a 100%, keep up the good work.'

            message = beginning+header+body+footer+xfactor_message

            record['points_recap'] = message

    @api.depends('create_date')
    def _compute_xfactor_recap(self):
        for record in self:
            user_id = record['task_id']['user_id'].id
            employee = record.env['hr.employee'].search([('user_id','=',user_id)])
            xfactor = employee['x_factor_value']
            beginning='<h2>X Factor: '+str(round(xfactor*100))+'%</h2><br/>'
            header = '<table class="table table-hover table-striped"><tr><th colspan="3">X Factor Detail:</th></tr>'
            body=''
            #getting each xfactor Category
            categories =  record.env['x_factor_categories'].search([])
            for category in categories:
                category_id = category.id
                xfactor = record.env['x_factor_journal'].search([('user_id','=',user_id),('x_factor_category','=',category_id)], limit=1, order='create_date desc')
                if len(xfactor)>= 1:
                    line = "<tr><td>"+xfactor['x_factor_category']['name']+"</td><td>"+str(round(xfactor['x_factor_value']*100))+"%</td><td>"+str(round(xfactor['points_attributed']))+"/"+str(round(xfactor['maximum_value_from_this_category_1']))+"</td></tr>"

                    body = body+line

            record['xfactor_recap'] = beginning+header+body


class ProductTags(models.Model):
    _name='product.tags'
    _description = 'Product Tags'

    name = fields.Char(string='Name')
    active = fields.Boolean(string='Active', default=True)
    sequence = fields.Integer(string='Sequence')


class System(models.Model):
    _name='cap.system'
    _description = 'System'

    name = fields.Char(string='Name')
    active = fields.Boolean(string='Active', default=True)
    location_id = fields.Many2one('res.partner', string='Location', ondelete='set null', copy=True)
    image = fields.Binary(string='Image')
    tags_ids = fields.Many2many('cap.tags', 'system_tag_rel', 'syatem_id', 'tag_id', string='Tags')
    sequence = fields.Integer(string='Sequence')
    notes = fields.Text(string='Notes')


class Tags(models.Model):
    _name='cap.tags'
    _description = 'Tags'

    name = fields.Char(string='Name')
    active = fields.Boolean(string='Active', default=True)
    color = fields.Integer(string='Color', copy=True, store=True)
    covered_by_monstercare_coverage_ = fields.Boolean(string='Covered by MonsterCare coverage ?')
    description = fields.Text(string='Description')
    sequence = fields.Integer(string='Sequence')
    notes = fields.Text(string='Notes')


class FactorCategories(models.Model):
    _name='factor.categories'
    _description = 'Factor Categories'

    active = fields.Boolean(string='Active', default=True)
    image = fields.Binary(string='Image')
    name = fields.Char(string='Name')
    maximum_value = fields.Float(string='Maximum Value')
    description = fields.Text(string='Description')
    sequence = fields.Integer(string='Sequence')


class FactorJournal(models.Model):
    _name='factor.journal'
    _description = 'Factor Journal'

    active = fields.Boolean(string='Active', default=True)
    date = fields.Date(string='Date', copy=True)
    image = fields.Binary(string='Image')
    name = fields.Char(string='Name')
    points_attributed = fields.Float(string='Points Attributed')
    x_factor_value = fields.Float(compute='_compute_x_factor_value', string='X Factor value', store=True)
    user_id = fields.Many2one('res.users', string='User', ondelete='set null')
    sequence = fields.Integer(string='Sequence')
    notes = fields.Text(string='Notes')
    x_factor_category_id = fields.Many2one('factor.categories', string='X Factor Category')
    maximum_value_from_this_category_1 = fields.Float(related='x_factor_category_id.maximum_value', store=True, string='Maximum value from this category')

    @api.depends('__last_update')
    def _compute_x_factor_value(self):
        for record in self: 
            if (record['x_factor_category']['maximum_value'])!= 0:
                record['x_factor_value'] = record['points_attributed']/record['x_factor_category']['maximum_value']


class SystemTags(models.Model):
    _name='system.tags'
    _description = 'System Tags'

    name = fields.Char(string='Name')
    color = fields.Integer(string='Color', copy=True, store=True)
    sequence = fields.Integer(string='Sequence')


class Point(models.Model):
    _name='cap.point'
    _description = 'Point'

    name = fields.Char(string='Name')
    date = fields.Date(string='Date', copy=True)
    x_factor_taken_into_account = fields.Boolean(string='X Factor taken into account ?')
    attribution_date = fields.Date(string='Attribution Date')
    x_factor_value_at_this_moment = fields.Float(compute='_compute_value_at_this_moment', string='X Factor value at this moment', store=True)
    points_after_xfactor = fields.Float(compute='_compute_points_after_xfactor', string='Final Value')
    points_attributed = fields.Float(string='Points Attributed')
    point_category_id = fields.Many2one('points.categories', string='Points Category')
    maximum_value_from_this_category = fields.Integer(related='point_category_id.maximum_points', string='Maximum value from this category', store=True)
    user_id = fields.Many2one('res.users', string='User', ondelete='set null')
    task_id = fields.Many2one('project.task', string='Task ID', ondelete='set null')
    sequence = fields.Integer(string='Sequence')
    notes = fields.Text(string='Notes')

    @api.depends('__last_update')
    def _compute_value_at_this_moment(self):
        for record in self:
            employee = self.env['hr.employee'].search([('user_id','=',record['user_id'].id)])
            record['x_factor_value_at_this_moment'] = employee['x_factor_value']

    @api.depends('create_date')
    def _compute_points_after_xfactor(self):
        for record in self:
            if record['x_factor_taken_into_account']:
                user_xfactor = self.env['hr.employee'].search([('user_id','=',record['user_id'].id)])['x_factor_value']
                record['points_after_xfactor'] = user_xfactor*record['points_attributed']
            else:
                record['points_after_xfactor'] = record['points_attributed']


class WeeklyGoals(models.Model):
    _name='weekly.goals'
    _description = 'Weekly Goals'

    name = fields.Char(string='Name')
    notes = fields.Text(string='Notes')
    sequence = fields.Integer(string='Sequence')
    yearly_goal_percentage = fields.Float(string='Yearly Goal Percentage')
    week_number = fields.Integer(string='Week Number')
