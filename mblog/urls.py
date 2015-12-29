from django.conf.urls import include, url, patterns
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from mblogApp.views import *

urlpatterns = patterns('',
	url(r'^$', index),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^login$', loginController, name='loginController'),
    url(r'^register$', registerController, name='registerController'),
	url(r'^nojavascript$', noJSController, name='noJSController'),
	url(r'^profile/(?P<username>\w{0,50})/$', profileController, name='profileController'),
	url(r'^tag/(?P<tagname>\w{0,50})/$', tagController, name='tagController'),
	url(r'^post/load$', infinityPostController, name='infinityPostController'),
)



