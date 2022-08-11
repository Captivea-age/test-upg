odoo.define('cap_task_gantt_customization.CustomGanttRow', function (require) {
    "use strict";

    var GanttRow = require('web_gantt.GanttRow');
    var core = require('web.core');
    var session = require('web.session');
    var Widget = require('web.Widget');
    const pyUtils = require('web.py_utils');
    let pyUtilsContext = null;

    var QWeb = core.qweb;
    var _t = core._t;

    GanttRow.include({

        init: function (parent, pillsInfo, viewInfo, options) {
            this._super.apply(this, arguments);
            var self = this;

            this.name = pillsInfo.groupName;
            this.groupId = pillsInfo.groupId;
            this.groupLevel = pillsInfo.groupLevel;
            this.groupedByField = pillsInfo.groupedByField;
            this.pills = _.map(pillsInfo.pills, _.clone);
            this.resId = pillsInfo.resId;

            this.viewInfo = viewInfo;
            this.fieldsInfo = viewInfo.fieldsInfo;
            this.state = viewInfo.state;
            this.colorField = viewInfo.colorField;

            this.options = options;
            this.SCALES = options.scales;
            this.isGroup = options.isGroup;
            this.isOpen = options.isOpen;
            this.rowId = options.rowId;
            this.unavailabilities = (options.unavailabilities || []).map(u => {
                return {
                    startDate: self._convertToUserTime(u.start),
                    stopDate: self._convertToUserTime(u.stop)
                };
            });

            this.consolidate = options.consolidate;
            this.consolidationParams = viewInfo.consolidationParams;

            if(options.thumbnail){
                this.thumbnailUrl = session.url('/web/image', {
                    model: options.thumbnail.model,
                    id: this.resId,
                    field: this.options.thumbnail.field,
                });
            }

            // the total row has some special behaviour
            this.isTotal = this.groupId === 'groupTotal';

            this._adaptPills();
            this._newAddPills();
            this._snapToGrid(this.pills);
            this._calculateLevel();
            if (this.isGroup && this.pills.length) {
                this._aggregateGroupedPills();
            } else {
                this.progressField = viewInfo.progressField;
                this._evaluateDecoration();
            }
            this._calculateMarginAndWidth();

            // Add the 16px odoo window default padding.
            this.leftPadding = (this.groupLevel + 1) * this.LEVEL_LEFT_OFFSET;
            this.cellHeight = this.level * this.LEVEL_TOP_OFFSET + (this.level > 0 ? this.level - 1 : 0);

            this.MIN_WIDTHS = { full: 100, half: 50, quarter: 25 };
            this.PARTS = { full: 1, half: 2, quarter: 4 };

            this.cellMinWidth = this.MIN_WIDTHS[this.viewInfo.activeScaleInfo.precision];
            this.cellPart = this.PARTS[this.viewInfo.activeScaleInfo.precision];

            this._prepareSlots();
            this._insertIntoSlot();

            this.childrenRows = [];

            this._onButtonAddClicked = _.debounce(this._onButtonAddClicked, 500, true);
            this._onButtonPlanClicked = _.debounce(this._onButtonPlanClicked, 500, true);
            this._onPillClicked = _.debounce(this._onPillClicked, 500, true);

            if (this.isTotal) {
                const maxCount = Math.max(...this.pills.map(p => p.count));
                const factor = maxCount ? (90 / maxCount) : 0;
                for (let p of this.pills) {
                    p.totalHeight = factor * p.count;
                }
            }
            this.isRTL = _t.database.parameters.direction === "rtl";
            if(pillsInfo.user_color_data){
                this.user_color = pillsInfo.user_color_data.filter(coldata => coldata.user_id == this.resId);
                if(this.user_color[0]){
                    this.user_color = this.user_color[0].color;
                }
            }
        },

        _newAddPills:function () {
            var newSlots = [];
            this.pills.forEach(function (currentPill) {
                if (currentPill.start_drive && currentPill.end_drive){
                    var obj_rec = Object.assign({'dateFirst': 'hello'}, currentPill)
                    obj_rec.startDate = currentPill.start_drive
                    obj_rec.stopDate = currentPill.end_drive
                    obj_rec.topPadding = 30 + 'px';
                    newSlots.push(obj_rec)
                }
                if (currentPill.start_job && currentPill.end_job){
                    var obj_rec = Object.assign({'dateSec': 'hello'}, currentPill)
                    obj_rec.startDate = currentPill.start_job
                    obj_rec.stopDate = currentPill.end_job
                    obj_rec.topPadding = 30 + 'px';
                    newSlots.push(obj_rec)
                }
                currentPill.topPadding = 30 + 'px';
                newSlots.push(currentPill)

            });
            this.pills = newSlots
        },

        _adaptPills: function () {
            var self = this;
            var dateStartField = this.state.dateStartField;
            var dateStopField = this.state.dateStopField;
            var ganttStartDate = this.state.startDate;
            var ganttStopDate = this.state.stopDate;
            this.pills.forEach(function (pill) {
                //FOR First Date
                if (pill['end_drive'] && pill['start_drive']){
                    pill['end_drive'] = self._convertToUserTime(pill['end_drive']);
                    pill['start_drive'] = self._convertToUserTime(pill['start_drive']);
                }
                //FOR Second Date
                if (pill['end_job'] && pill['start_job']){
                    pill['end_job'] = self._convertToUserTime(pill['end_job']);
                    pill['start_job'] = self._convertToUserTime(pill['start_job']);
                }
                var pillStartDate = self._convertToUserTime(pill[dateStartField]);
                var pillStopDate = self._convertToUserTime(pill[dateStopField]);
                if (pillStartDate < ganttStartDate) {
                    pill.startDate = ganttStartDate;
                    pill.disableStartResize = true;
                } else {
                    pill.startDate = pillStartDate;
                }
                if (pillStopDate > ganttStopDate) {
                    pill.stopDate = ganttStopDate;
                    pill.disableStopResize = true;
                } else {
                    pill.stopDate = pillStopDate;
                }
                // Disable resize feature for groups
                if (self.isGroup) {
                    pill.disableStartResize = true;
                    pill.disableStopResize = true;
                }
            });
        },

        _calculateMarginAndWidth: function () {
            var self = this;
            var left;
            var diff;
            this.pills.forEach(function (pill) {
                switch (self.state.scale) {
                    case 'day':
                        left = pill.startDate.diff(pill.startDate.clone().startOf('hour'), 'minutes');
                        pill.leftMargin = (left / 60) * 100;
                        diff = pill.stopDate.diff(pill.startDate, 'minutes');
                        var gapSize = pill.stopDate.diff(pill.startDate, 'hours') - 1; // Eventually compensate border(s) width
                        pill.width = gapSize > 0 ? 'calc(' + (diff / 60) * 100 + '% + ' + gapSize + 'px)' : (diff / 60) * 100 + '%';
                        // Custom date Calculation
                        if (pill.start_drive && pill.end_drive){
                            var hours = pill.start_drive.clone().startOf('hour')
                            pill.date1 = true;
                            left = pill.start_drive.diff(pill.start_drive.clone().startOf('hour'), 'minutes');
                            pill.date1_left = (left / 60) * 100;
                            diff = pill.end_drive.diff(pill.start_drive, 'minutes');
                            var gapSize = pill.end_drive.diff(pill.start_drive, 'hours') - 1; // Eventually compensate border(s) width
                            pill.date1_width = gapSize > 0 ? 'calc(' + (diff / 60) * 100 + '% + ' + gapSize + 'px)' : (diff / 60) * 100 + '%';

                        }else{
                            pill.date1_left = false;
                            pill.date1_width = false;
                        }

                        if (pill.start_job && pill.end_job){
                            left = pill.start_job.diff(pill.start_job.clone().startOf('hour'), 'minutes');
                            pill.date2_left = (left / 60) * 100;
                            diff = pill.end_job.diff(pill.start_job, 'minutes');
                            var gapSize = pill.end_job.diff(pill.start_job, 'hours') - 1; // Eventually compensate border(s) width
                            pill.date2_width = gapSize > 0 ? 'calc(' + (diff / 60) * 100 + '% + ' + gapSize + 'px)' : (diff / 60) * 100 + '%';
                        }else{
                            pill.date2_left = false;
                            pill.date2_width = false;
                        }

                        break;
                    case 'week':
                    case 'month':
                        left = pill.startDate.diff(pill.startDate.clone().startOf('day'), 'hours');
                        pill.leftMargin = (left / 24) * 100;
                        diff = pill.stopDate.diff(pill.startDate, 'hours');
                        var gapSize = pill.stopDate.diff(pill.startDate, 'days') - 1; // Eventually compensate border(s) width
                        pill.width = gapSize > 0 ? 'calc(' + (diff / 24) * 100 + '% + ' + gapSize + 'px)' : (diff / 24) * 100 + '%';
                        break;
                    case 'year':
                        var startDateMonthStart = pill.startDate.clone().startOf('month');
                        var stopDateMonthEnd = pill.stopDate.clone().endOf('month');
                        left = pill.startDate.diff(startDateMonthStart, 'days');
                        pill.leftMargin = (left / 30) * 100;

                        var monthsDiff = stopDateMonthEnd.diff(startDateMonthStart, 'months', true);
                        if (monthsDiff < 1) {
                            // A 30th of a month slot is too small to display
                            // 1-day events are displayed as if they were 2-days events
                            diff = Math.max(Math.ceil(pill.stopDate.diff(pill.startDate, 'days', true)), 2);
                            pill.width = (diff / pill.startDate.daysInMonth()) * 100 + "%";
                        } else {
                            // The pill spans more than one month, so counting its
                            // number of days is not enough as some months have more
                            // days than others. We need to compute the proportion
                            // of each month that the pill is actually taking.
                            var startDateMonthEnd = pill.startDate.clone().endOf('month');
                            var diffMonthStart = Math.ceil(startDateMonthEnd.diff(pill.startDate, 'days', true));
                            var widthMonthStart = (diffMonthStart / pill.startDate.daysInMonth());

                            var stopDateMonthStart = pill.stopDate.clone().startOf('month');
                            var diffMonthStop = Math.ceil(pill.stopDate.diff(stopDateMonthStart, 'days', true));
                            var widthMonthStop = (diffMonthStop / pill.stopDate.daysInMonth());

                            var width = Math.max((widthMonthStart + widthMonthStop), (2 / 30)) * 100;
                            if (monthsDiff > 2) { // start and end months are already covered
                                // If the pill spans more than 2 months, we know
                                // that the middle months are fully covered
                                width += (monthsDiff - 2) * 100;
                            }
                            pill.width = width + "%";
                        }
                        break;
                    default:
                        break;
                }

                // Add 1px top-gap to events sharing the same cell.
                pill.topPadding = pill.level * (self.LEVEL_TOP_OFFSET + 1);
            });
        },

        _calculateLevel: function () {
            var self = this
            if (this.isGroup || !this.pills.length) {
                // We want shadow pills to overlap each other
                this.level = 0;
                this.pills.forEach(function (pill) {
                    pill.level = 0;
                });
            } else {
                // Sort pills according to start date
                this.pills = _.sortBy(this.pills, 'startDate');
                this.pills[0].level = 0;
                var levels = [{
                    pills: [this.pills[0]],
                    maxStopDate: this.pills[0].stopDate,
                }];
                for (var i = 1; i < this.pills.length; i++) {
                    var currentPill = this.pills[i];
                    for (var l = 0; l < levels.length; l++) {
                        if (currentPill.startDate >= levels[l].maxStopDate) {
                            currentPill.level = l;
                            levels[l].pills.push(currentPill);
                            if (currentPill.stopDate > levels[l].maxStopDate) {
                                levels[l].maxStopDate = currentPill.stopDate;
                            }
                            break;
                        }
                    }
                    if (!currentPill.level && currentPill.level != 0) {
                        currentPill.level = levels.length;
                        levels.push({
                            pills: [currentPill],
                            maxStopDate: currentPill.stopDate,
                        });
                    }
                }
                this.pills.forEach(function (pill) {
                    self.pills.forEach(function (rec) {
                        if (rec.display_name == pill.display_name){
                            rec.level = pill.level;
                        }
                    });
                });
                this.level = levels.length;
            }
        },

        _bindPillPopover: function(target) {
            var self = this;
            var $target = $(target);
            if (!$target.hasClass('o_gantt_pill')) {
                $target = this.$(target.offsetParent);
            }
            if ($target.hasClass('dateFirst')){
                $target.popover({
                    container: this.$el,
                    trigger: 'hover',
                    delay: {show: this.POPOVER_DELAY},
                    html: true,
                    placement: 'auto',
                    content: function () {
                        return self.viewInfo.popoverQWeb.render('gantt-popover-dateFirst', self._getPopoverContext($(this).data('id')));
                    },
                }).popover("show");
            }else if ($target.hasClass('dateSec')){
                $target.popover({
                    container: this.$el,
                    trigger: 'hover',
                    delay: {show: this.POPOVER_DELAY},
                    html: true,
                    placement: 'auto',
                    content: function () {
                        return self.viewInfo.popoverQWeb.render('gantt-popover-dateSec', self._getPopoverContext($(this).data('id')));
                    },
                }).popover("show");
            }else {
                $target.popover({
                    container: this.$el,
                    trigger: 'hover',
                    delay: {show: this.POPOVER_DELAY},
                    html: true,
                    placement: 'auto',
                    content: function () {
                        return self.viewInfo.popoverQWeb.render('gantt-popover', self._getPopoverContext($(this).data('id')));
                    },
                }).popover("show");
            }
        },

        _getPopoverContext: function (pillID) {
            var data = _.clone(_.findWhere(this.pills, {id: pillID}));
            data.userTimezoneStartDate = this._convertToUserTime(data[this.state.dateStartField]);
            data.userTimezoneStopDate = this._convertToUserTime(data[this.state.dateStopField]);
            data.userTimezoneStartDrive = data["start_drive"] ? this._convertToUserTime(data["start_drive"]) : false;
            data.userTimezoneStopDrive = data["end_drive"] ? this._convertToUserTime(data["end_drive"]) : false;
            data.userTimezoneStartJob = data["start_job"] ? this._convertToUserTime(data["start_job"]) : false;
            data.userTimezoneStopJob = data["end_job"] ? this._convertToUserTime(data["end_job"]) : false;
//            data.userTimezoneStartDrive = this._convertToUserTime(data["start_drive"]);
//            data.userTimezoneStopDrive = this._convertToUserTime(data["end_drive"]);
//            data.userTimezoneStartJob = this._convertToUserTime(data["start_job"]);
//            data.userTimezoneStopJob = this._convertToUserTime(data["end_job"]);
            return data;
        },
    })
});
