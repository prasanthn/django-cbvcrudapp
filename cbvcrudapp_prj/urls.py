from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'cbvcrudapp_prj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^cbvcrudapp/', include('cbvcrudapp.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

# Use Django to serve media and static files --- even when DEBUG == False. In
# production environment configure server to serve from these URLs so that the
# request never reaches Django. Heroku's Python example project repo recommends
# these settings, along with gunicorn as server.
from django.conf import settings
static_url = settings.STATIC_URL.lstrip('/').rstrip('/')
urlpatterns += patterns(
    '',
    (r'^%s/(?P<path>.*)$' % static_url, 'django.views.static.serve',
     {
         'document_root': settings.STATIC_ROOT,
     }),
)
media_url = settings.MEDIA_URL.lstrip('/').rstrip('/')
urlpatterns += patterns(
    '',
    (r'^%s/(?P<path>.*)$' % media_url, 'django.views.static.serve',
        {
            'document_root': settings.MEDIA_ROOT,
        }),
)
