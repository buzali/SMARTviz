from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import TemplateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'smart_viz.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^events/eventbrite/(?P<ll>[-]?\d+\.\d+,[-]?\d+\.\d+)?', 'events.views.eventbrite'),
    url(r'^events/foursquare/(?P<ll>[-]?\d+\.\d+,[-]?\d+\.\d+)?', 'events.views.foursquare'),
    url(r'^events/meetups/(?P<ll>[-]?\d+\.\d+,[-]?\d+\.\d+)?', 'events.views.meetups'),
    url(r'^events/songkick/(?P<ll>[-]?\d+\.\d+,[-]?\d+\.\d+)?', 'events.views.songkick'),
    url(r'^events/(?P<ll>[-]?\d+\.\d+,[-]?\d+\.\d+)?$', 'events.views.index'),
    url(r'^showtimes/(?P<ll>[-]?\d+\.\d+,[-]?\d+\.\d+)?', 'events.views.showtimes'),
    url(r'^related/facebook/(?P<searchQuery>[^\/]+)', 'related.views.facebook'),
    url(r'^related/twitter/(?P<searchQuery>[^\/]+)', 'related.views.twitter'),
    url(r'^related/instagram/(?P<searchQuery>[^\/]+)', 'related.views.instagram'),
    url(r'^related/instaloco/(?P<lat>[^\/]+)/(?P<lng>[^\/]+)', 'related.views.instaloco'),
    url(r'^related/places/(?P<lat>[^\/]+)/(?P<lng>[^\/]+)/(?P<typey>[^\/]+)/(?P<searchTerm>[^\/]+)', 'related.views.places'),
    url(r'^related/places/(?P<lat>[^\/]+)/(?P<lng>[^\/]+)/(?P<typey>[^\/]+)', 'related.views.places'),
    url(r'^related/createCalendar/(?P<myUserId>[^\/]+)', 'related.views.createCalendar'),
    url(r'^related/createEvent/(?P<desc>[^\/]+)/(?P<startDate>[^\/]+)/(?P<endDate>[^\/]+)/(?P<location>[^\/]+)/(?P<myCalendarId>[^\/]+)', 'related.views.createEvent'),
    url(r'^related/deleteEvent/(?P<eventId>[^\/]+)/(?P<myCalendarId>[^\/]+)', 'related.views.deleteEvent'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^about/', 'smartviz.views.about'),
    url(r'^$', 'smartviz.views.index'),
)
