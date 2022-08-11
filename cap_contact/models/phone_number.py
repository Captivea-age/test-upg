from odoo import models, fields, api, _


class PhoneNumber(models.Model):
    _name="phone.number"
    _description = 'Phone Number'

    partner_id = fields.Many2one('res.partner', string="Contact")
    phone = fields.Char(string="Phone")
    type = fields.Selection([('phone','Landline'),('mobile','Mobile'),('other','Other')],string="Type")
    tags = fields.Many2many(comodel_name="phone.number.tag",relation='phone_tags_rel',)
    display_in_job = fields.Boolean(string="Display in Jobs ?")


class ResPartner(models.Model):
    _inherit="res.partner"

    phone_number_ids = fields.One2many('phone.number','partner_id',string="Phone numbers")


class PhoneNumberTags(models.Model):
    _name = "phone.number.tag"
    _description = 'Phone Number Tags'

    name= fields.Char(string="Tag name")
