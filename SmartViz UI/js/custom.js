$(document).ready(function(){

    // hide event-sidebar on load
    $(".event-sidebar").hide();

    // hide main-sidebar and show event-sidebar
    $(".events-nearby-container").click( function() {
        $(".main-sidebar").hide();
        $(".event-sidebar").show();
    });

    // hide main-sidebar and show event-sidebar
    $(".restaurants-nearby-container").click( function() {
        $(".main-sidebar").hide();
        $(".event-sidebar").show();
    });

    // show main-sidebar and hide event-sidebar
    $(".back-button").click( function() {
        $(".event-sidebar").hide();
        $(".main-sidebar").show();
    });
});
