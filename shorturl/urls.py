from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'surl.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'surl.views.root', name='root'),
    url(r'', include('surl.urls')),
)
