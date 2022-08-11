odoo.define('cap_gantt_view_changes.custom_gatt_form', function (require) {
"use strict";
var custom_gatt_view_form = require('web_gantt.GanttRow');
custom_gatt_view_form.include({
_prepareSlots: function () {
        const { interval, time, cellPrecisions } = this.SCALES[this.state.scale];
        const precision = this.viewInfo.activeScaleInfo.precision;
        const cellTime = cellPrecisions[precision];

        function getSlotStyle(cellPart, subSlotUnavailabilities, isToday) {
            function color(d) {
                if (isToday) {
                    return d ? '#f4f3ed' : '#fffaeb';
                }
                return d ? '#e9ecef' : '#ffffff';
            }
            const sum = subSlotUnavailabilities.reduce((acc, d) => acc + d);
            if (!sum) {
                return '';
            }
            if (cellPart === sum) {
                return `background: ${color(1)}`;
            }
            if (cellPart === 2) {
                const [c0, c1] = subSlotUnavailabilities.map(color);
                return `background: linear-gradient(90deg, ${c0} 49%, ${c1} 50%);`
            }
            if (cellPart === 4) {
                const [c0, c1, c2, c3] = subSlotUnavailabilities.map(color);
                return `background: linear-gradient(90deg, ${c0} 24%, ${c1} 25%, ${c1} 49%, ${c2} 50%, ${c2} 74%, ${c3} 75%);`
            }
        }

        this.slots = [];

        // We assume that the 'slots' (dates) are naturally ordered
        // and that unavailabilties have been normalized
        // (i.e. naturally ordered and pairwise disjoint).
        // A subslot is considered unavailable (and greyed) when totally covered by
        // an unavailability.
        let index = 0;
        for (const date of this.viewInfo.slots) {
            const slotStart = date;
            const slotStop = date.clone().add(1, interval);
            const isToday = date.isSame(new Date(), 'day') && this.state.scale !== 'day';

            let slotStyle = '';
            if (!this.isGroup && this.unavailabilities.slice(index).length) {
                let subSlotUnavailabilities = [];
                for (let j = 0; j < this.cellPart; j++) {
                    const subSlotStart = date.clone().add(j * cellTime, time);
                    const subSlotStop = date.clone().add((j + 1) * cellTime, time).subtract(1, 'seconds');
                    let subSlotUnavailable = 0;
                    for (let i = index; i < this.unavailabilities.length; i++) {
                        let u = this.unavailabilities[i];
                        if (subSlotStop > u.stopDate) {
                            index++;
                        } else if (u.startDate <= subSlotStart) {
                            subSlotUnavailable = 1;
                            break;
                        }
                    }
                    subSlotUnavailabilities.push(subSlotUnavailable);
                }
                slotStyle = getSlotStyle(this.cellPart, subSlotUnavailabilities, isToday);
            }
            this.slots.push({
                isToday: isToday,
                style: slotStyle,
                hasButtons: !this.isGroup && !this.isTotal,
                start: slotStart,
                stop: slotStop,
                pills: [],
            });


        }

        if (this.slots.length == 24) {
    this.slots.splice(21, 3);
    this.slots.splice(0, 7);
    this.viewInfo.slots.splice(21, 3);
    this.viewInfo.slots.splice(0, 7);
}

    },
});
});