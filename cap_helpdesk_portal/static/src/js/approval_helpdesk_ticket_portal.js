odoo.define('cap_helpdesk_portal.ApprovalHelpdeskTicketPortal', function (require) {
'use strict';

var publicWidget = require('web.public.widget');
const Dialog = require('web.Dialog');
const {_t, qweb} = require('web.core');
const ajax = require('web.ajax');

publicWidget.registry.ticketPortalApproval = publicWidget.Widget.extend({
    selector: '.o_portal_helpdesk_ticket',
    events: {
        "click #close": '_onClickClose',
        "click #keep_open": '_onClickKeepOpen',
        "click #send_feedback": '_onClickSendFeedback',
    },

    _onClickClose: function (ev) {
        ajax.jsonRpc('/web/dataset/call_kw_helpdesk', 'call', {
            model: 'helpdesk.ticket',
            method: 'write',
            args: [
                [parseInt(ev.target.dataset.ticket_id)], {'stage_id': 25, 'customer_closure_approval': true, 'page_visited': true}
            ],
            kwargs: {}
        }).then(function (result) {
            window.location.href = window.location.origin + '/approval/submitted'
        });
    },

    _onClickKeepOpen: function (ev) {
        var x = this.$el.find(".div_open")
        console.log($(x))
        if (x[0].style.display === "none") {
            x[0].style.display = "block";
        } else {
            x[0].style.display = "none";
        }
    },

     _onClickSendFeedback: function (ev) {
        this._rpc({
            route: '/update/helpdesk_ticket',
            params: {
                ticket_id: parseInt(ev.target.dataset.ticket_id),
                message: $.trim(this.$el.find("#description").val()),
            },
        }).then(function (result) {
           window.location.href = window.location.origin + '/approval/send_feedback'
        });
    },
});


});
