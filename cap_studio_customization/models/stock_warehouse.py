# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class StockWarehouse(models.Model):
    _inherit='stock.warehouse'

    appear_on_aor_truck_assignment = fields.Boolean(string='Appear on AOR Truck assignment ?')