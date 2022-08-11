# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    categorys = fields.Char(string='Category ID(s)')
    code = fields.Char(string='Code')
    category_name = fields.Char(string='Category Name')
    unit_of_measure = fields.Char(string='Unit of Measure')
    job_category = fields.Char(string='Job Category')
    job_code = fields.Char(string='Job Code')
    tag_ids = fields.Many2many('product.tags', 'product_template_product_tags_rel', 'template_id', 'tag_id', string='Tags')
    tags_model_ids = fields.Many2many('cap.tags', 'product_template_tags_rel', 'template_id', 'tag_id', string='Tags')
    visible_on_customer_invoice = fields.Boolean(string='Visible on customer invoice')
