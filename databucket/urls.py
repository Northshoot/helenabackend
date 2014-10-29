'''
Created on Oct 28, 2014

@author: lauril
'''
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'databucket.views.home', name='home'),
    url(r'^firestorm/list/(?P<amount>\w+)/$', 'databucket.views.firestorm', name="firestorm"),
    url(r'^firestorm/add/$', 'databucket.views.firestormAdd', name="firestormAdd"),

)