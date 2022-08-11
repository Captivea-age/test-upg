from odoo import http
from odoo.addons.web.controllers.main import DataSet


class DataSet(DataSet):

    @http.route(['/web/dataset/call_kw_helpdesk', '/web/dataset/call_kw_helpdesk/<path:path>'], type='json', auth="public")
    def call_kw_purchase(self, model, method, args, kwargs, path=None):
        return self._call_kw(model, method, args, kwargs)
