from odoo import models, fields, api, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def update_prices(self):
        self.ensure_one()
        lines_to_update = []

        for line in self.order_line.filtered(lambda line: not line.display_type):
            product = line.product_id.with_context(
                partner=self.partner_id,
                quantity=line.product_uom_qty,
                date=self.date_order,
                pricelist=self.pricelist_id.id,
                uom=line.product_uom.id
            )

            price_unit = self.env['account.tax']._fix_tax_included_price_company(
                line._get_display_price(product), line.product_id.taxes_id, line.tax_id, line.company_id)

            if self.pricelist_id.discount_policy == 'without_discount' and price_unit:
                price_discount_unrounded = self.pricelist_id.get_product_price(product, line.product_uom_qty, self.partner_id, self.date_order, line.product_uom.id)
                main_price = line.price_reduce
                if main_price > price_unit:
                    discount = max(0, (main_price - price_unit) * 100 / main_price)
                else:
                    discount = max(0, (price_unit - price_discount_unrounded) * 100 / price_unit)
            else:
                discount = 0

            lines_to_update.append((1, line.id, {'price_unit': price_unit, 'discount': discount}))
        self.update({'order_line': lines_to_update})
        self.show_update_pricelist = False
        self.message_post(body=_("Product prices have been recomputed according to pricelist <b>%s<b> ", self.pricelist_id.display_name))

