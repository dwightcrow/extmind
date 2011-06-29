from extmind import settings
from django.conf.urls.defaults import *
from django.contrib import admin

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'learn.views.queue'),
    (r'^queue/$', 'learn.views.queue'),
    (r'^concepts/$', 'learn.views.concepts'),
    (r'^session/$', 'learn.views.session'),
    (r'^calendar/$', 'learn.views.calendar'),
    url(r'^admin/', include(admin.site.urls)),
)

# need to change for production XXX_DWIGHT
if True:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', 
         {'document_root': '/home/dwight/extmind/learn/static/'}), 
    )
