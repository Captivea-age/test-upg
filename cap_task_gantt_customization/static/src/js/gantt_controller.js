odoo.define('cap_gantt_view_changes.CustomGanttController', function (require) {
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
            'click .o_gantt_button_prev': '_onPrevPeriodClicked',
        }),
        /**
         * @private
         * @param {MouseEvent} ev
         */
        _onDatePickerClicked: function (ev) {
            ev.preventDefault();
            this.update({date: moment($(ev.target).val()) });
        },
        renderButtons: function ($node) {
        var state = this.model.get();
        this.$buttons = $(QWeb.render('GanttView.buttons', {
            groupedBy: state.groupedBy,
            widget: this,
            SCALES: this.SCALES,
            activateScale: state.scale,
            allowedScales: this.allowedScales,
        }));
        var now = new Date();
        var day = ("0" + now.getDate()).slice(-2);
        var month = ("0" + (now.getMonth() + 1)).slice(-2);
        var today = now.getFullYear()+"-"+(month)+"-"+(day);
        var o_gantt_date_picker = this.$buttons.find('.o_gantt_date_picker')[0];
        console.log("today")
        console.log(today)
        o_gantt_date_picker.value = today;
        if ($node) {
            this.$buttons.appendTo($node);
        }
    },


        _onTodayClicked: function (ev) {
            ev.preventDefault();
            var now = new Date();
            var day = ("0" + now.getDate()).slice(-2);
            var month = ("0" + (now.getMonth() + 1)).slice(-2);
            var today = now.getFullYear()+"-"+(month)+"-"+(day) ;
            $(".o_gantt_date_picker").val(today);
            this.update({ date: moment() });
        },

        _onPrevPeriodClicked: function (ev) {
             ev.preventDefault();
            var state = this.model.get();
            var subtract_date = state.focusDate.subtract(1, state.scale);
            this.update({ date: subtract_date });

            var prev_day = subtract_date;
            var day = ("0" + prev_day._d.getDate()).slice(-2);
            var month = ("0" + (prev_day._d.getMonth() + 1)).slice(-2);
            var prev_date = prev_day._d.getFullYear()+"-"+(month)+"-"+(day) ;

            $(".o_gantt_date_picker")[0].value = prev_date;
        },

        _onNextPeriodClicked: function (ev) {
            ev.preventDefault();
            var state = this.model.get();
            var add_date = state.focusDate.add(1, state.scale);
            this.update({ date: add_date });
            var next_day = add_date;
            var day = ("0" + next_day._d.getDate()).slice(-2);
            var month = ("0" + (next_day._d.getMonth() + 1)).slice(-2);
            var next_date = next_day._d.getFullYear()+"-"+(month)+"-"+(day) ;
            $(".o_gantt_date_picker")[0].value = next_date;

        },
    });
});
