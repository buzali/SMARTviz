from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'smart_viz.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^events/(?P<ll>[-]?\d+\.\d+,[-]?\d+\.\d+)?', 'events.views.index'),
	url(r'^related/', 'related.views.index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name='test.html')),
)
