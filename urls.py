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
    (r'^saveText/(?P<conceptId>.*)$', 'learn.views.saveText'),
    (r'^settings/$', 'learn.views.settings'),
    (r'^saveSettings/$', 'learn.views.saveSettings'),
    (r'^register/$', 'learn.views.register'),
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'learn.views.logout'),
    url(r'^admin/', include(admin.site.urls)),
)

# need to change for production XXX_DWIGHT
if True:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', 
         {'document_root': '/home/dwight/extmind/learn/static/'}), 
    )
