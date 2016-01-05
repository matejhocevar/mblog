from django.conf.urls import include, url, patterns
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from mblogApp.views import *


urlpatterns = patterns('',
	url(r'^$', index),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^login/$', loginController, name='loginController'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^register/$', registerController, name='registerController'),

	url(r'^nojavascript$', noJSController, name='noJSController'),

	url(r'^profile/$', profileController, name='profileController'),
	url(r'^profile/(?P<username>\w{0,50})/$', profileController, name='profileController'),
	url(r'^profile/(?P<username>\w{0,50})/edit/$', editProfileController, name='subscribeController'),
	url(r'^profile/(?P<username>\w{0,50})/(?P<mode>\w{0,50})/$', subscribeController, name='subscribeController'),

	url(r'^tag/(?P<tagname>\w{0,250})/$', tagController, name='tagController'),
	url(r'^post/load/$', infinityPostController, name='infinityPostController'),
	url(r'^post/add/$', postController, name='postController'),

	url(r'^search/$', searchController, name='searchController'),
	url(r'^search/(?P<query>\w{0,1024})/$', searchController, name='searchController'),

	url(r'^fill/(?P<model>\w{0,20})/(?P<number>\d{0,10})/$', fillController, name='fillController'),
	url(r'^fill/(?P<model>\w{0,20})/(?P<number>\d{0,10})/(?P<author>\d{0,10})/$', fillController, name='fillController'),
	url(r'^fill/(?P<model>\w{0,20})/(?P<number>\d{0,10})/(?P<author>\d{0,10})/(?P<time>\w{0,20})/$', fillController, name='fillController'),
)


