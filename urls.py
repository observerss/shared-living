from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^accounts/',include('modules.accounts.urls')),
    (r'^living/', include('living.urls')),
    (r'^changelog/$', direct_to_template,
           { 'template': 'changelog.html' }, 'changelog'),
    (r'^about/$', direct_to_template,
           { 'template': 'about.html' }, 'about'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),

    #templates
    (r'^$', direct_to_template,
           { 'template': 'index.html' }, 'index'),

    #static serve
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}),

)
