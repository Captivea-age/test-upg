# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
_logger = logging.getLogger(__name__)

class MaterialPopup(models.Model):
    _name='material.popup'
    _description = 'Material Popup'

    product_category_id = fields.Many2one('product.category',string='Category')
    product_sub_category_id = fields.Many2one('product.category',string='Sub category')
    task_id = fields.Many2one('project.task', string='Job')

    product_list_ids = fields.Many2many('product.list',compute='_compute_product_list_ids', store=True)
    search_field = fields.Char(string="Product name")


    @api.onchange('product_category_id')
    def reset_sub_category(self):
        self.product_sub_category_id = False
        self.product_list_ids = False

    @api.depends('product_sub_category_id', 'product_category_id')
    def _compute_product_list_ids(self):
        if self.product_category_id: 
            self.update({
                        'product_list_ids': False
                    })
            products = self.env['product.product'].search([('categ_id','=',self.product_category_id.id)])
            if len(products)>0:
                self.update({
                    'product_list_ids':[(0, 0, {'product_id': product.id, 'quantity': 0}) for product in products]
                })
            else:
                self.update({
                    'product_list_ids':False
                })

            if self.product_sub_category_id :
                products = self.env['product.product'].search([('categ_id','=',self.product_sub_category_id.id)])
                if len(products)>0:
                    self.update({
                        'product_list_ids':[(0, 0, {'product_id': product.id, 'quantity': 0}) for product in products]
                    })
                else:
                    self.update({
                        'product_list_ids': False
                    })
        else:
            self.update({
                    'product_list_ids': False
                })

        return True

    # def saveMaterial(self):
    #     # for product_line in self.product_list_ids.filtered(lambda product: product.quantity != 0):
    #     #     product_line.product_id.set_fsm_quantity(product_line.quantity)
    #     #     _logger.warning('Added %s qty for %s'%(product_line.quantity,product_line.product_id.name ))
    #     for product_line in self.product_list_ids:
    #         #product_line.product_id.set_fsm_quantity(product_line.quantity)
    #         _logger.warning('Added %s qty for %s'%(product_line.quantity,product_line.product_id.name ))


    #     # for product_line in self.product_list_ids.filtered(lambda product: product.quantity == 0):
    #     #     product_line.unlink()
    #     # return True


    def searchMaterial(self):
        search_field = self.search_field
        self.update({
                    'product_list_ids':False
                })
        product_list = self.env['product.product'].search(['|',('name','ilike',search_field),'|',('description','ilike',search_field),('default_code','ilike',search_field)])
        self.update({
            'product_list_ids':[(0, 0, {'product_id': product.id, 'quantity': 0}) for product in product_list.filtered(lambda product: product.type != 'service') ]
        })


        return {
            'type': 'ir.actions.act_window',
            'res_model': 'material.popup',
            'view': 'material_popup_form_view',
            'view_mode':'form',
            'target': 'new',
            'res_id':self.id,
        }


class ProductList(models.Model):
    _name = 'product.list'
    _description = 'Product List'

    product_id = fields.Many2one('product.product',string="Material")
    quantity = fields.Integer(string="Quantity")

    @api.onchange('quantity')
    def _onchange_quantity(self):
       # self.update({'quantity': self.quantity})            
        _logger.warning('Changed %s qty for %s via the @api.onchange'%(self.quantity,self.product_id.name ))
        self.product_id.set_fsm_quantity(self.quantity)
