from django.conf.urls import include, url, patterns
from django.contrib import admin
from mblogApp.views import *


urlpatterns = patterns('',
	url(r'^$', index),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^login', loginController, name='loginController'),
    url(r'^register', registerController, name='registerController'),
	url(r'^profile/(?P<username>\w{0,50})/$', profileController, name='profileController'),
	url(r'^tag/(?P<tagname>\w{0,50})/$', tagController, name='tagController'),
)