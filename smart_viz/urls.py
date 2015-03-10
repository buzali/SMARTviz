from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import TemplateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'smart_viz.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^events/(?P<ll>[-]?\d+\.\d+,[-]?\d+\.\d+)?', 'events.views.index'),
	url(r'^related/facebook/(?P<searchQuery>[^\/]+)', 'related.views.facebook'),
	url(r'^related/twitter/(?P<searchQuery>[^\/]+)', 'related.views.twitter'),
	url(r'^related/instagram/(?P<searchQuery>[^\/]+)', 'related.views.instagram'),
	url(r'^related/instaloco/(?P<lat>[^\/]+)/(?P<lng>[^\/]+)', 'related.views.instaloco'),
	url(r'^related/places/(?P<lat>[^\/]+)/(?P<lng>[^\/]+)/(?P<typey>[^\/]+)/(?P<searchTerm>[^\/]+)', 'related.views.places'),
	url(r'^related/places/(?P<lat>[^\/]+)/(?P<lng>[^\/]+)/(?P<typey>[^\/]+)', 'related.views.places'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'smartviz.views.index'),
)
