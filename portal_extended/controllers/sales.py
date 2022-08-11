from odoo import fields, http, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager
from odoo.osv import expression



class SaleOrder():
    _ihnerit="sale.order"
    def search(self, args, offset=0, limit=None, order=None, count=False):
        """ search(args[, offset=0][, limit=None][, order=None][, count=False])

        Searches for records based on the ``args``
        :ref:`search domain <reference/orm/domains>`.

        :param args: :ref:`A search domain <reference/orm/domains>`. Use an empty
                     list to match all records.
        :param int offset: number of results to ignore (default: none)
        :param int limit: maximum number of records to return (default: all)
        :param str order: sort string
        :param bool count: if True, only counts and returns the number of matching records (default: False)
        :returns: at most ``limit`` records matching the search criteria

        :raise AccessError: * if user tries to bypass access rules for read on the requested object.
        """
        args = args[:-1]
        args+= ",('portal_access_ids','=',partner.id)]"
        res = self._search(args, offset=offset, limit=limit, order=order, count=count)
        return res if count else self.browse(res)

class CustomerPortal(CustomerPortal):

    # def _document_check_access(self, model_name, document_id, access_token=None):
    #     #adding partner id
    #     partner = request.env.user.partner_id
    #
    #     document = request.env[model_name].browse([document_id])
    #     document_sudo = document.with_user(SUPERUSER_ID).exists()
    #     if not document_sudo:
    #         raise MissingError(_("This document does not exist."))
    #
    #     try:
    #         document.check_access_rights('read')
    #         document.check_access_rule('read')
    #     except AccessError:
    #         if
    #         if not access_token or not document_sudo.access_token or not consteq(document_sudo.access_token, access_token):
    #             raise
    #     #Adding the check if the contact is in the contact list
    #     if model_name == 'sale.order':
    #         if partner_id in document_id
    #     return document_sudo


    @http.route(['/my/orders', '/my/orders/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_orders(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        SaleOrder = request.env['sale.order']

        [('message_partner_ids','child_of',[user.commercial_partner_id.id])]


        domain = [
            ('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),
            ('state', 'in', ['sale', 'done']),
            ('user_id','in','portal_access_ids.ids')
        ]

        searchbar_sortings = {
            'date': {'label': _('Order Date'), 'order': 'date_order desc'},
            'name': {'label': _('Reference'), 'order': 'name'},
            'stage': {'label': _('Stage'), 'order': 'state'},
        }

        # default sortby order
        if not sortby:
            sortby = 'date'
        sort_order = searchbar_sortings[sortby]['order']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # count for pager
        order_count = SaleOrder.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/orders",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=order_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager
        orders = SaleOrder.search(domain, order=sort_order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_orders_history'] = orders.ids[:100]

        values.update({
            'date': date_begin,
            'orders': orders.sudo(),
            'page_name': 'order',
            'pager': pager,
            'default_url': '/my/orders',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        return request.render("sale.portal_my_orders", values)
