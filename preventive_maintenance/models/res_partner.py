# -- coding: utf-8 --
from odoo import models, fields, api, _
from datetime import date, datetime, timedelta
import logging
logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    system_ids = fields.One2many('preventive_maintenance.system','location_id',string='Systems list')
