odoo.define('cap_gantt_view_changes.GanttController', function (require) {
    "use strict";

    var AbstractController = require('web.AbstractController');
    var GanttController = require('web_gantt.GanttController');
    var core = require('web.core');
    var dialogs = require('web.view_dialogs');
    var confirmDialog = require('web.Dialog').confirm;

    var QWeb = core.qweb;
    var _t = core._t;

    GanttController.include({
        events: _.extend({}, GanttController.prototype.events, {
            'change .o_gantt_date_picker': '_onDatePickerClicked',
        }),
        /**
         * @private
         * @param {MouseEvent} ev
         */
        _onDatePickerClicked: function (ev) {
            ev.preventDefault();
            this.update({ date: moment($(ev.target).val()) });
        },
    });
});