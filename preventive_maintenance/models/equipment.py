

from odoo import models, fields, api, _


class Equipment(models.Model):

    _name = "preventive_maintenance.equipment"
    _description = "Equipment model"

    name = fields.Char("Equipment Name")
    section_id = fields.Many2one("preventive_maintenance.section", string="Equipment Section")
    option_group = fields.Char(string="Option Group")
    option_name = fields.Char(string="Option Name")
    system_category = fields.Selection([('ac','AC'),('hp','HP')], string="System category")
    equipment_health = fields.Selection([('good','Good'),('warning','Warning'),('error','Error')],string="Equipment Health", readonly=True)
    equipment_type_ids = fields.Many2many(model_name='preventive_maintenance.system_type', relation='pm_equipments_system_types_rel', string="Equipment Types")
    cpm = fields.Integer(string="Cubic Feet per Minute")

    install_date = fields.Date(string="Install date")
    brand_id = fields.Many2one("preventive_maintenance.brand",string="Brand")
    #model_id = fields.Many2one("preventive_maintenance.brand.model",string="Model")
    model_id = fields.Char(string="Model")
    serial_number = fields.Char("Serial #")