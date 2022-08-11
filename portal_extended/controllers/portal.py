# -*- coding: utf-8 -*-

from odoo import fields, http, _
from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class LocationsCustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'locations_count' in counters:
            values['locations_count'] = len(
                request.env.user.partner_id.location_list_ids.mapped('location_id'))
        return values

    @http.route(['/my/locations', '/my/locations/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_locations(self, page=1, sortby=None, filterby=None, search=None, search_in='all', groupby='none',
                            **kw):
        values = self._prepare_portal_layout_values()
        _items_per_page = 100

        locations_count = len(request.env.user.partner_id.location_list_ids.mapped('location_id'))
        # pager
        pager = portal_pager(
            url="/my/locations",
            url_args={'sortby': sortby, 'search_in': search_in, 'search': search, 'filterby': filterby,
                      'groupby': groupby},
            total=locations_count,
            page=page,
            step=_items_per_page
        )

        locations = request.env.user.partner_id.location_list_ids.mapped('location_id')

        location_system = request.env['preventive_maintenance.system'].sudo().search(
            [('location_id', 'in', locations.ids)])

        values.update({
            'locations': locations,
            'page_name': 'locations',
            'location_system': location_system,
            'default_url': '/my/locations',
            'pager': pager,
            'search_in': search_in,
            'search': search,
            'sortby': sortby,
            'groupby': groupby,
            'filterby': filterby,
        })
        return request.render("portal_extended.portal_my_locations", values)
