# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import logging
logger = logging.getLogger(__name__)


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    page_visited = fields.Boolean(string='Page Visited')
