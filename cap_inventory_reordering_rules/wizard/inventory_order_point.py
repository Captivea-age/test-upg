from odoo import api, fields, models, _


class InventoryOrderpoint(models.TransientModel):
    _name = "inventory.order.point"

    product_ids = fields.Many2many('product.product', domain="[('type','=','product')]", required=True)
    location_ids = fields.Many2many('stock.location', required=True)
    location_type_ids = fields.Many2many('stock.location.type', required=True)
    product_min_qty = fields.Integer(string="Min Quantity", required=True)
    product_max_qty = fields.Integer(string="Max Quantity", required=True)
    qty_multiple = fields.Integer("Multiple Quantity", required=True)

    def create_reordering_rules(self):
        vals = []
        for product in self.product_ids:
            for location_type in self.location_type_ids:
                for location in location_type.location_ids:
                    recs = self.env['stock.warehouse.orderpoint'].search([
                        ('product_id', '=', product.id), ('location_id', '=', location.id)])
                    recs.write({'active': False})
                    vals.append({'product_id': product.id,
                                 'location_id': location.id,
                                 'product_min_qty': self.product_min_qty,
                                 'product_max_qty': self.product_max_qty,
                                 'qty_multiple': self.qty_multiple})
        self.env['stock.warehouse.orderpoint'].create(vals)

        return {
            'view_mode': 'tree',
            'res_model': 'stock.warehouse.orderpoint',
            'type': 'ir.actions.act_window',
        }

class StockLocationType(models.Model):
    _name = 'stock.location.type'

    name = fields.Char(string="Type name")
    location_ids = fields.One2many('stock.location','location_type_id',string="Location list") 

class StockLocation(models.Model):
    _inherit = 'stock.location'

    location_type_id = fields.Many2one('stock.location.type',string="Location type")
