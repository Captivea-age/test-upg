odoo.define('cap_gantt_view_changes.GanttModel', function (require) {
    "use strict";

    var AbstractModel = require('web.AbstractModel');
    var GanttModel = require('web_gantt.GanttModel');
    var core = require('web.core');
    var fieldUtils = require('web.field_utils');
    const utils = require('web.utils');
    var session = require('web.session');

    var _t = core._t;
    
    GanttModel.include({
        _getFields: function () {

            var fields = ['display_name', this.ganttData.dateStartField, this.ganttData.dateStopField];
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

            fields.push(
                'x_studio_job_notes',
                'x_studio_job_type', 
                'partner_id', 
                'schedule_ready', 
                'tags_to_char', 
                'x_studio_customer_name', 
                'name',
                'x_studio_start_drive',
                'x_studio_arrived_at_location',
                'x_studio_job_finished'
               );
            return _.uniq(fields);
        },
    });
});