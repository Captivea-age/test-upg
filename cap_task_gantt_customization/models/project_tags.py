# -*- coding: utf-8 -*-
from odoo import models, fields
from odoo import http
from odoo.http import request
import json


class GanttViewControllers(http.Controller):
    @http.route('/get_user_color', auth='public', type='json')
    def get_user_color(self):
        get_color = request.env['res.users'].sudo().search([])
        color_dict = {}
        color_list = []
        for user_id in get_color:
            if user_id.team_color.color:
                vals = {'user_id': user_id.id, 'color': user_id.team_color.color}
                color_list.append(vals)
        return json.dumps(color_list)


class ProjectStageTags(models.Model):
    _inherit = 'project.task.type'

    color = fields.Integer(string="Stage Color")
