// Startup Scripts
var old_json = null;

// update calendar data with Tofi's JSON
function updateCalendarData(tofi_json) {

    if (old_json) {
        $('#calendar').fullCalendar( 'removeEventSource', old_json);
    }

    updated_json = changeTofiData(tofi_json);
    old_json = updated_json;

    // In order to refresh calendar, first remove event source and then add it back again
    $('#calendar').fullCalendar( 'removeEventSource');
    $('#calendar').fullCalendar( 'addEventSource', updated_json);
    $("#calendar").fullCalendar( 'refetchEvents' );
    $("a.fc-event").attr("target", "_blank");
}


// change "name" to "title" in tofi's json
function changeTofiData(tofi_json) {
    var title;
    for(var i = 0; i < tofi_json.length; i++) {
        if(tofi_json[i].hasOwnProperty("name")) {
            tofi_json[i]["title"] = tofi_json[i]["name"];
            delete tofi_json[i]["name"];
        }
    }
    return tofi_json;
}


$(document).ready(function()
{
    // Javascript for customizing default date to today
    //
    // var d = new Date();
    // var month = d.getMonth()+1;
    // var day = d.getDate();
    // var default_date = d.getFullYear() + '-' +
    // (month<10 ? '0' : '') + month + '-' +
    // (day<10 ? '0' : '') + day;
    // console.log (default_date);


    // =====================================================
    // For the calendar view, we are using FullCalendar.io
    // Docs: http://fullcalendar.io/docs/
    // =====================================================

    var updated_json;

    // default calendar setup
    $('#calendar').fullCalendar({
            //defaultDate: default_date,
            editable: true,
            eventLimit: true, // allow "more" link when too many events
            events: updated_json,
            eventAfterAllRender: function(view) {
                if (parent.calendarhack)
                    updateCalendarData(parent.calendarhack);
            }
    });

    // Sample value for Tofi's JSON
    /*var tofi_json = [{"end": "2015-04-05T16:15:00+01:00", "name": "Improve your teaching skills using Rubrics: A Dynamic approach", "url": "http://www.eventbrite.co.uk/e/improve-your-teaching-skills-using-rubrics-a-dynamic-approach-tickets-16560170917?aff=ebapi", "photo": null, "longitude": "-0.12775829999998223", "start": "2015-04-05T09:30:00+01:00", "latitude": "51.5073509", "type": "Eventbrite", "description": "2015-04-05T09:30:00+01:00 - 2015-04-05T16:15:00+01:00"},
        {"end": "2015-04-20T16:00:00+01:00", "name": "Kundalini Kriya Yoga Retreat and Special Chakra Meditation", "url": "http://www.eventbrite.co.uk/e/kundalini-kriya-yoga-retreat-and-special-chakra-meditation-tickets-16319020630?aff=ebapi", "photo": null, "longitude": "-0.1278", "start": "2015-04-05T17:00:00+01:00", "latitude": "51.5074", "type": "Eventbrite", "description": "2015-04-05T17:00:00+01:00 - 2015-04-20T16:00:00+01:00"}];



    // call this function to update calendar data
    updateCalendarData(tofi_json);*/



    // =====================================================
    // For the datepicker, we are using Bootstrap Datepicker
    // Docs: https://bootstrap-datepicker.readthedocs.org/en/latest/
    // =====================================================

    // Setup for Bootstrap datepicker
    $('#datepicker').datepicker({
        format: 'mm-dd-yyyy',
        autoclose: true,
        todayHighlight: true
    });

    // Registering event handler for datepicker
    $('#datepicker').datepicker()
    .on('changeDate', dateChanged);

    // When user picks a new date, reload all the data
    function dateChanged(e) {
        console.log(e.date);
        console.log(e.date.getFullYear());
        // Note that javascript months start from 0
        console.log(e.date.getMonth());
        console.log(e.date.getDate());

        // when date is changed, get new events
        // Make sure to add events to calendar when user stars it.
    }
});

