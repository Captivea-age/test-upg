# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json
import math

from odoo import http
from odoo.http import request


class Helpdesk(http.Controller):

    @http.route(["/approval/<int:ticket_id>", ], type='http', auth="public", methods=['GET', 'POST'], website=True)
    def approval_ticket(self, ticket_id=None, **post):
        rec_id = int(math.sqrt((ticket_id+8)/8))
        ticket = request.env['helpdesk.ticket'].browse(rec_id)
        if ticket.page_visited:
            return request.render("cap_helpdesk_portal.approval_done")
        return request.render("cap_helpdesk_portal.helpdesk_ticket_approval", {'ticket': ticket})

    @http.route(["/update/helpdesk_ticket", ], type='json', auth="public", methods=['GET', 'POST'], website=True)
    def update_data(self, ticket_id, message, **post):
        ticket = request.env['helpdesk.ticket'].browse(ticket_id)
        ticket.sudo().write(
            {'stage_id': 24, 'priority': str(int(ticket.priority) + 1) if int(ticket.priority) < 3 else ticket.priority,
             'page_visited': True})
        request.env['mail.message'].sudo().create({
            'body': message,
            'model': 'helpdesk.ticket',
            'res_id': ticket.id,
            'message_type': 'comment',
            'subtype_id': request.env['ir.model.data'].xmlid_to_res_id('mail.mt_note'),
        })
        return json.dumps(True)

    @http.route(["/approval/submitted", ], type='http', auth="public", methods=['GET', 'POST'], website=True)
    def approval_submitted(self, **post):
        return request.render("cap_helpdesk_portal.approval_thanks")

    @http.route(["/approval/send_feedback", ], type='http', auth="public", methods=['GET', 'POST'], website=True)
    def approval_send_feedback(self, **post):
        return request.render("cap_helpdesk_portal.approval_send_feedback")
