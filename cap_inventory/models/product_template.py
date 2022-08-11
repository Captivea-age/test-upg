# -*- coding: utf-8 -*-
import logging
import requests
import json
# from requests.auth import HTTPBasicAuth
from requests.structures import CaseInsensitiveDict
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    
    _inherit='product.template'

    stocked = fields.Boolean('Stocked product')