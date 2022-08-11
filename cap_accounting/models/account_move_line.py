from odoo import models, fields, api, _


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.model
    def _get_price_total_and_subtotal_model(self, price_unit, quantity, discount, currency, product, partner, taxes,
                                            move_type):
        res = {}
        # Compute 'price_subtotal'.
        if not self.sale_line_ids.order_id.pricelist_id or self.sale_line_ids.order_id.pricelist_id.discount_policy != 'without_discount':
            line_discount_price_unit = price_unit * (1 - (discount or 0.0) / 100.0)
        else:
            price = self.sale_line_ids._get_display_price(product)
            line_discount_price_unit = self.sale_line_ids.price_unit

        subtotal = quantity * line_discount_price_unit
        res['price_unit'] = line_discount_price_unit
        # Compute 'price_total'.
        if taxes:
            force_sign = -1 if move_type in ('out_invoice', 'in_refund', 'out_receipt') else 1
            taxes_res = taxes._origin.with_context(force_sign=force_sign).compute_all(line_discount_price_unit,
                quantity=quantity, currency=currency, product=product, partner=partner, is_refund=move_type in ('out_refund', 'in_refund'))
            res['price_subtotal'] = taxes_res['total_excluded']
            res['price_total'] = taxes_res['total_included']
        else:
            res['price_total'] = res['price_subtotal'] = subtotal
        #In case of multi currency, round before it's use for computing debit credit
        if currency:
            res = {k: currency.round(v) for k, v in res.items()}
        return res