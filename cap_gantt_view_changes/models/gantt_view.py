from odoo import models, fields, api, _

class GanttViewTaskImage(models.Model):
    _inherit = "project.task"

    tag_image = fields.Binary(string="Task Image")
    tags_to_char = fields.Char(string="Tags To Char", compute="_compute_tags_char")

    def _compute_tags_char(self):
        for rec in self:
            ftag = ''
            if len(rec.x_studio_tags) > 0:
                for tag in rec.x_studio_tags:
                    ftag += str(tag.name) + ", "
            rec.tags_to_char = ftag
            