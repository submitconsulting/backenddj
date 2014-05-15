from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'backenddj.views.home', name='home'),
    url(r'^$', 'apps.home.views.index', name='index'),
    # url(r'^blog/', include('blog.urls')),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
        
    url(r'^accounts/password_reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    url(r'^accounts/password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    # Support old style base36 password reset links; remove in Django 1.7
    url(r'^accounts/reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm_uidb36'),
    url(r'^accounts/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm',
        name='password_reset_confirm'),
    url(r'^accounts/reset/done/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),
    
    #url(r'^accounts/', include('django.contrib.auth.urls')), # esto no pk solo quiero manejar pass reset
    
    # Apss del mod Backend
    url(r'^params/', include('apps.params.urls')),
    url(r'^space/', include('apps.space.urls')),
    url(r'^sad/', include('apps.sad.urls')),
    url(r'^accounts/', include('apps.accounts.urls')),
    url(r'^home/', include('apps.home.urls')),
    url(r'^mod_backend/', include('apps.mod_backend.urls')),
    
    # Apss del mod ventas
    url(r'^maestros/', include('apps.maestros.urls')),
    url(r'^mod_ventas/', include('apps.mod_ventas.urls')),
    
    # Apss del mod profesional
    url(r'^rrhh/', include('apps.rrhh.urls')),
    url(r'^mod_pro/', include('apps.mod_pro.urls')),
    
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT, }),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': settings.DEBUG}),
    
)