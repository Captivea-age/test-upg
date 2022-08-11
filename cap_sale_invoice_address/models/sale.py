# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = 'sale.order'

    default_values_done = fields.Boolean(string="Default values done")
    tech_manual_quotation = fields.Boolean(string="Tech manual quotation", default=False)

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        super().onchange_partner_id()
        #### ABDE's changes - Adding the correct invoice address
        if self.task_id and not self.default_values_done:
            self.partner_id = self.task_id.partner_id.id
            self.payment_term_id = 1

            #Getting quotation template
            if self.task_id.job_type_id.default_quotation_template and not self.tech_manual_quotation:
                self.sale_order_template_id = self.task_id.job_type_id.default_quotation_template.id
            elif not self.tech_manual_quotation:
                template = self.env['sale.order.template'].search([('name','=','Default Service')],limit=1)
                self.sale_order_template_id = template.id



            #Getting all the customer that have the "Bill to" for this location
            customer_list = self.env['contact.location.relationship'].search([
                ('location_id', '=', self.task_id.partner_id.id),
                ('contact_roles_ids', 'in', self.env['contact.role'].search([('name', '=', 'Bill to')]).ids)])

            #If no one to invoice, invoice the actual customer
            if len(customer_list) == 0:
                partner_invoice_id = self.task_id.partner_id.id
                #Else invoice the last person tagged as "Bill to"
            else:
                partner_invoice_id = customer_list[0].contact_id.id

            self.update({
                'payment_term_id':1,
                'partner_invoice_id':partner_invoice_id,
                'partner_shipping_id':partner_invoice_id,
                'default_values_done':True,
              })

            if self.sale_order_template_id:
                self.onchange_sale_order_template_id()
        else:
            self.default_values_done = True
