

from odoo import models, fields, api, _


class Component(models.Model):

    _name = "preventive_maintenance.component"
    _description = "Component model"

    name = fields.Char(string="Component Name")
    section_id = fields.Many2one("preventive_maintenance.section", string="Component Section")
    component_sub_category = fields.Char(string="Component Sub Category")
    service_life = fields.Integer(string="Service Life")
    component_options = fields.Many2many(comodel_name="preventive_maintenance.equipment",relation='pm_components_equipments_rel',string="Option tags")
