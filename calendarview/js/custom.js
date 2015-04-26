// Startup Scripts
$(document).ready(function()
{

    var events_json = [{title: 'GSA Wine Tasting', start: '2015-04-29T16:00:00-04:00', url: 'http://google.com'},
    {title: 'New Time', start: '2015-04-29T17:00:00', url: 'http://google.com'}];

    var d = new Date();
    var month = d.getMonth()+1;
    var day = d.getDate();

    var default_date = d.getFullYear() + '-' +
    (month<10 ? '0' : '') + month + '-' +
    (day<10 ? '0' : '') + day;
    console.log (default_date);

    // default calendar setup
	$('#calendar').fullCalendar({
            defaultDate: default_date,
            editable: true,
            eventLimit: true, // allow "more" link when too many events
            events: events_json
    });

    // making calendar links open in new tab
    $("a.fc-day-grid-event").attr("target", "_BLANK");

    // Make sure to add events to calendar when user stars it.

    // Setup for Bootstrap datepicker
    $('#datepicker').datepicker({
        format: 'mm-dd-yyyy',
        autoclose: true,
        todayHighlight: true
    });

    // When date is change
    $('#datepicker').datepicker()
    .on('changeDate', dateChanged);

    function dateChanged(e) {
        console.log(e.date);
        console.log(e.date.getFullYear());
        // Note that javascript months start from 0
        console.log(e.date.getMonth());
        console.log(e.date.getDate());

        // when date is changed, get new events
        // prefill today's date.
    }

    // html to add a new event
});

/*
[
                {
                    title: 'All Day Event',
                    start: '2015-02-01'
                },
                {
                    title: 'Long Event',
                    start: '2015-02-07',
                    end: '2015-02-10'
                },
                {
                    id: 999,
                    title: 'Repeating Event',
                    start: '2015-02-09T16:00:00'
                },
                {
                    id: 999,
                    title: 'Repeating Event',
                    start: '2015-02-16T16:00:00'
                },
                {
                    title: 'Conference',
                    start: '2015-02-11',
                    end: '2015-02-13'
                },
                {
                    title: 'Meeting',
                    start: '2015-02-12T10:30:00',
                    end: '2015-02-12T12:30:00'
                },
                {
                    title: 'Lunch',
                    start: '2015-02-12T12:00:00'
                },
                {
                    title: 'Meeting',
                    start: '2015-02-12T14:30:00'
                },
                {
                    title: 'Happy Hour',
                    start: '2015-02-12T17:30:00'
                },
                {
                    title: 'Dinner',
                    start: '2015-02-12T20:00:00'
                },
                {
                    title: 'Birthday Party',
                    start: '2015-02-13T07:00:00'
                },
                {
                    title: 'Click for Google',
                    url: 'http://google.com/',
                    start: '2015-02-28'
                }
            ]
 */
