from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^cdot_count/$', 'CrowdedMountain.apps.cdot_counting.views.ugly_count', name='CDOT count'),
    url(r'^$', 'CrowdedMountain.apps.mountain_chooser.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),

    # Examples:
    #url(r'^$', 'CrowdedMountain.views.home', name='home'),
    # url(r'^CrowdedMountain/', include('CrowdedMountain.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
