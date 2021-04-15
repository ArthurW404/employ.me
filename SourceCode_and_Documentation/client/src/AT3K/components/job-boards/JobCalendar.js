import moment from 'moment';
import React, { useState } from 'react';
import { Calendar, momentLocalizer } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import calendarStyles from './JobCalendar.module.scss';

import FullscreenMode from './FullscreenMode';

// Google Calendar API documentation: https://developers.google.com/calendar
// React Calendar component documentation: https://www.npmjs.com/package/react-calendar
// This one may be better: http://jquense.github.io/react-big-calendar/examples/index.html

const localizer = momentLocalizer(moment);

const JobCalendar = ({ trackedJobs }) => {
    let events = [];
    trackedJobs.forEach(job => {
        return job.events.forEach(event => {
            events = [...events, {
                title: `${event.name} | ${job.title}`,
                start: new Date(event.time * 1000),
                end: new Date(event.time * 1000)
            }];
        });
    });
    return (
        <FullscreenMode>
            <div className={calendarStyles.container}>
                <Calendar
                    localizer={localizer}
                    events={events}
                    startAccessor="start"
                    endAccessor="end"
                    style={{ height: 500 }}
                />
            </div>
        </FullscreenMode>
    );
};

export default JobCalendar;
