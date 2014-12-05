from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'djangoproject_soccer_power_ranking.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin', include(admin.site.urls)),
    url(r'^app_soccer_power_ranking/', include('app_soccer_power_ranking.urls')), # ADD THIS NEW TUPLE!
)
