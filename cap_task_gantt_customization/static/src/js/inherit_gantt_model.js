odoo.define('cap_task_gantt_customization.CustomGanttModel', function (require) {
    "use strict";
    var GanttModel = require('web_gantt.GanttModel');
    var AbstractModel = require('web.AbstractModel');
    var concurrency = require('web.concurrency');
    var core = require('web.core');
    var fieldUtils = require('web.field_utils');
    const utils = require('web.utils');
    var session = require('web.session');
    var rpc = require('web.rpc');
    var ajax = require('web.ajax');

    var _t = core._t;

GanttModel.include({

    _fetchData: function () {
        var self = this;
        var domain = this._getDomain();
        var context = Object.assign({}, this.context, { group_by: this.ganttData.groupedBy });
        var groupsDef;
        if (this.ganttData.groupedBy.length) {
            groupsDef = this._rpc({
                model: this.modelName,
                method: 'read_group',
                fields: this._getFields(),
                domain: domain,
                context: context,
                groupBy: this.ganttData.groupedBy,
                orderBy: this.ganttData.groupedBy.map(function (f) { return {name: f}; }),
                lazy: this.ganttData.groupedBy.length === 1,
            });
        }
        var get_user_colors = ajax.jsonRpc('/get_user_color', 'call', {})
//        var helpdesk_tag_data = ajax.jsonRpc('/get_helpdesk_tags', 'call', {})
        var dataDef = this._rpc({
            route: '/web/dataset/search_read',
            model: this.modelName,
            fields: this._getFields(),
            context: context,
            domain: domain,
        });

        return this.dp.add(Promise.all([groupsDef, dataDef,get_user_colors])).then(function (results) {
            var groups = results[0];
            var searchReadResult = results[1];
            var user_color_ids = JSON.parse(results[2])

            if (groups) {
                _.each(groups, function (group) {
                    group.id = _.uniqueId('group');
                });
            }
            var oldRows = self.allRows;
            self.allRows = {};
            self.ganttData.groups = groups;
            self.ganttData.records = self._parseServerData(searchReadResult.records);
            self.ganttData.rows = self._generateRows({
                groupedBy: self.ganttData.groupedBy,
                groups: groups,
                oldRows: oldRows,
                records: self.ganttData.records,
                user_color:user_color_ids,
            });
            var unavailabilityProm;
            if (self.displayUnavailability && !self.isSampleModel) {
                unavailabilityProm = self._fetchUnavailability();
            }
            return unavailabilityProm;
        });
    },

    _generateRows: function (params) {
        var self = this;
        var groups = params.groups;
        var groupedBy = params.groupedBy;
        var rows;
        if (!groupedBy.length) {
            // When no groupby, all records are in a single row
            var row = {
                groupId: groups && groups.length && groups[0].id,
                id: _.uniqueId('row'),
                records: params.records,
            };
            rows = [row];
            this.allRows[row.id] = row;
        } else {
            // Some groups might be empty (thanks to expand_groups), so we can't
            // simply group the data, we need to keep all returned groups
            var groupedByField = groupedBy[0];
            var currentLevelGroups = utils.groupBy(groups, groupedByField);
            const groupedRecords = utils.groupBy(params.records, groupedByField);
            rows = Object.keys(currentLevelGroups).map(function (key) {
                var subGroups = currentLevelGroups[key];
                var groupRecords = groupedRecords[key] || [];

                // For empty groups, we can't look at the record to get the
                // formatted value of the field, we have to trust expand_groups
                var value;
                if (groupRecords && groupRecords.length) {
                    value = groupRecords[0][groupedByField];
                } else {
                    value = subGroups[0][groupedByField];
                }

                var path = (params.parentPath || '') + JSON.stringify(value);
                var minNbGroups = self.collapseFirstLevel ? 0 : 1;
                var isGroup = groupedBy.length > minNbGroups;
                var row = {
                    name: self._getFieldFormattedValue(value, self.fields[groupedByField]),
                    groupId: subGroups[0].id,
                    groupedBy: groupedBy,
                    groupedByField: groupedByField,
                    id: _.uniqueId('row'),
                    resId: Array.isArray(value) ? value[0] : value,
                    isGroup: isGroup,
                    isOpen: !utils.findWhere(params.oldRows, { path: path, isOpen: false }),
                    path: path,
                    records: groupRecords,
                    user_color: params.user_color
                };

                // Generate sub groups
                if (isGroup) {
                    row.rows = self._generateRows({
                        groupedBy: groupedBy.slice(1),
                        groups: subGroups,
                        oldRows: params.oldRows,
                        parentPath: row.path + '\n',
                        records: groupRecords,
                        user_color: params.user_color,
                    });
                    row.childrenRowIds = [];
                    row.rows.forEach(function (subRow) {
                        row.childrenRowIds.push(subRow.id);
                        row.childrenRowIds = row.childrenRowIds.concat(subRow.childrenRowIds || []);
                    });
                }

                self.allRows[row.id] = row;

                return row;
            });
            if (!rows.length) {
                // we want to display an empty row in this case
                rows = [{
                    groups: [],
                    records: [],
                }];
            }
        }
        /*Custom Code [For remove undefined task rows] [start]*/
        _.each(rows, function(row){
            if(row.groupedByField === 'user_id' && !row.resId){
                row.name = _t('Unassigned Tasks');
                rows.pop();
            }
        });
        /*Custom Code [For remove undefined task rows] [end]*/
        return rows;
    },

    _getFields: function () {
        if (this.modelName == "project.task") {
            var fields = ['display_name', this.ganttData.dateStartField, this.ganttData.dateStopField, 'start_drive', 'end_drive', 'start_job', 'end_job'];
            fields = fields.concat(this.ganttData.groupedBy, this.decorationFields);

            if (this.progressField) {
                fields.push(this.progressField);
            }

            if (this.colorField) {
                fields.push(this.colorField);
            }

            if (this.consolidationParams.field) {
                fields.push(this.consolidationParams.field);
            }

            if (this.consolidationParams.excludeField) {
                fields.push(this.consolidationParams.excludeField);
            }

            /* Custom fields for gantt view*/
            fields.push('stage_id', 'schedule_ready','task_color','image_on_tag')
        }
        /* Custom fields for gantt view*/
        return _.uniq(fields);
    },
})
});
