'''
Created on Oct 28, 2014

@author: lauril
'''
from django.conf.urls import patterns, include, url
from django.contrib import admin
import autofixture
autofixture.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'databucket.views.home', name='home'),
    url(r'^firestorm/list/(?P<amount>\w+)/$', 'databucket.views.firestorm', name="firestorm"),
    url(r'^firestorm/add/(?P<action>\w+)/$', 'databucket.views.firestormAdd', name="firestormAdd"),
    url(r'^observations/(?P<fire_id>\w+)/$', 'databucket.views.observations', name="observations"),
    url(r'^analytics/$', 'databucket.views.analytics', name="analytics"),
    url(r'^heat/$', 'databucket.views.heat', name="heat"),
    url(r'^latest/(?P<amount>\d+)/$', 'databucket.views.latest', name="latest"),

)