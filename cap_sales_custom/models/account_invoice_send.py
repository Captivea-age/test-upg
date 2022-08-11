from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class AccountInvoiceSend(models.TransientModel):
    _inherit='account.invoice.send'

#     contact_list_ids = fields.One2many(related='res.partner.contact_list_ids')
    contact_list_ids = fields.One2many(related='partner_ids.contact_list_ids')
    contact_ids = fields.Many2many('res.partner',string='Contacts', compute="_compute_list_contacts")
    
    @api.depends('contact_list_ids')
    def _compute_list_contacts(self):
        for record in self:
            list = []
            for rel in record.contact_list_ids:
                list.append(rel.contact_id.id)
            record['contact_ids'] = list