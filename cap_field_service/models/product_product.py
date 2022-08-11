from odoo import models, fields, api, _


class ProductProduct(models.Model):
    _inherit = "product.product"

    user_warehouse = fields.Boolean(string='User Warehouse', compute='_compute_user_warehouse')
    user_warehouse_product = fields.Boolean(string='User Warehouse Product', compute='_compute_user_warehouse_product',store=True)
    store_qty_available = fields.Float(related='qty_available', store=True)

    def _compute_user_warehouse(self):
        self.user_warehouse = False
        if self.user_has_groups('stock.group_stock_multi_warehouses'):
            user_warehouse_location = self.env.user.property_warehouse_id.lot_stock_id
            stock_quant = self.env['stock.quant'].search([('location_id', '=', user_warehouse_location.id)])
            products = self.search([('id', 'in', stock_quant.mapped('product_id').ids)])
            if products:
                products.write({'user_warehouse': True})

    @api.depends('user_warehouse')
    def _compute_user_warehouse_product(self):
        for record in self:
            record.user_warehouse_product = False
            if record.user_warehouse:
                record.user_warehouse_product = record.user_warehouse

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        warehouse_products =  super(ProductProduct, self).search_read([('user_warehouse_product', '=', True)], fields=fields, offset=offset, limit=limit, order='store_qty_available asc')
        domain.append(['user_warehouse_product', '=', False])
        result = super(ProductProduct, self).search_read(domain=domain, fields=fields, offset=offset, limit=limit, order='user_warehouse_product desc')
        for warehouse_product in warehouse_products:
            result.insert(0, warehouse_product)
        return result
