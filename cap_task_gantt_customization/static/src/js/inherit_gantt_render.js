odoo.define('cap_task_gantt_customization.CustomGanttRenderer', function (require) {
    "use strict";

    var AbstractRenderer = require('web.AbstractRenderer');
    var config = require('web.config');
    var core = require('web.core');
    var GanttRenderer = require('web_gantt.GanttRenderer');
    var GanttRow = require('web_gantt.GanttRow');
    var qweb = require('web.QWeb');
    var session = require('web.session');
    var utils = require('web.utils');

    var QWeb = core.qweb;
    var _t = core._t;


    GanttRenderer.include({
        _renderRows: function (rows, groupedBy) {
            var self = this;
            var rowWidgets = [];
            var disableResize = this.state.scale === 'year';

            var groupLevel = this.state.groupedBy.length - groupedBy.length;
// FIXME: could we get rid of collapseFirstLevel in Renderer, and fully
// handle this in Model?
            var hideSidebar = groupedBy.length === 0;
            if (this.collapseFirstLevel) {
                hideSidebar = self.state.groupedBy.length === 0;
            }
            rows.forEach(function (row) {
                var pillsInfo = {
                    groupId: row.groupId,
                    resId: row.resId,
                    pills: row.records,
                    groupLevel: groupLevel,
                    user_color_data: row.user_color,
                };
                if (groupedBy.length) {
                    pillsInfo.groupName = row.name;
                    pillsInfo.groupedByField = row.groupedByField;

                }
                var params = {
                    canCreate: self.canCreate,
                    canCellCreate: self.canCellCreate,
                    canEdit: self.canEdit,
                    canPlan: self.canPlan,
                    isGroup: row.isGroup,
                    consolidate: (groupLevel === 0) && (self.state.groupedBy[0] === self.consolidationParams.maxField),
                    hideSidebar: hideSidebar,
                    isOpen: row.isOpen,
                    disableResize: disableResize,
                    disableDragdrop: self.disableDragdrop,
                    rowId: row.id,
                    scales: self.SCALES,
                    unavailabilities: row.unavailabilities,

                };
                if (self.thumbnails && row.groupedByField && row.groupedByField in self.thumbnails) {
                    params.thumbnail = {
                        model: self.fieldsInfo[row.groupedByField].relation,
                        field: self.thumbnails[row.groupedByField],
                    };
                }
                rowWidgets.push(self._renderRow(pillsInfo, params));
                if (row.isGroup && row.isOpen) {
                    var subRowWidgets = self._renderRows(row.rows, groupedBy.slice(1));
                    rowWidgets = rowWidgets.concat(subRowWidgets);
                }
            });
            return rowWidgets;
        },

        renderNowIndicator: function () {
            var self = this;
            // var gantt_var = self.$el.find(".o_gantt_view").prevObject[0];
            // gantt_var.style.overflow = "scroll";
            // gantt_var.style.width = "300%";
            var current_day = new Date();
            var current_hour = current_day.getHours();

            var scroll_div = document.querySelector('.o_content');
            if (scroll_div) {
                scroll_div.scrollLeft = (225 * current_hour)
                setTimeout(function () {
                    // var scroll_position = (225 * current_hour)
                    // if (scroll_div) {
                    scroll_div.scrollLeft = (225 * current_hour)
                    // }
                }, 120000);
            }

            if (self.state.scale == "day") {
                self.$el.find('span.gantt-day-now-indicator').remove();
                var height = self.$el[0].clientHeight - self.$el.find('.o_gantt_header_slots div:first')[0].clientHeight
                var indicator = $('<span></span>', {
                    class: 'gantt-day-now-indicator',
                    style: 'height: ' + height + 'px;'
                });
                var current_slot = self.$el.find('div.o_gantt_header_cell[data-hour=' + moment().format('k') + ']');
                current_slot.append($(indicator));
                if (moment().minute() <= 30) {
                    indicator.animate({
                        left: "10px",
                        right: "unset",
                    })
                } else {
                    indicator.animate({
                        right: "10px",
                        left: "unset",
                    })
                }
                setTimeout(function () {
                    self.renderNowIndicator();
                    self.indicator_delay = 1000 * 60;
                // }, self.indicator_delay);
                }, 600000);
            }
        },


        async _renderView() {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self.indicator_delay = (1000 * 60) - (moment().second() * 1000);
                self.renderNowIndicator();
            })
        },
    })
});
