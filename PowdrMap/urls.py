from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    url(r'^cdot_count/$', 'PowdrMap.apps.cdot_counting.views.ugly_count', name='CDOT count'),
    url(r'^$', 'PowdrMap.views.place_holder', name='place_holder'),
    #url(r'^$', 'PowdrMap.views.huge_place_holder', name='huge_place_holder'),
    #url(r'^admin/', include(admin.site.urls)),

    # Examples:
    #url(r'^$', 'PowdrMap.views.home', name='home'),
    # url(r'^PowdrMap/', include('PowdrMap.foo.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^inbox/notifications/', include(notifications.urls)),
    url(r'^user_sessions/', include('user_sessions.urls', 'user_sessions'))
)
