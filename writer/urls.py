# encoding=utf-8

from django.conf.urls import url, include
from writer import views

urlpatterns = [
    url(r'^$', views.index, name='w.index'),
    url(r'^login/?$', views.login, name='w.login'),
    url(r'^logout/?$', views.logout, name='w.logout'),
    url(r'^n/(?P<pk>\w+)/?$', views.novel, name='w.novel'),
    url(r'^n/(?P<pk>\w+)/c/(?P<seq>\d+)/?$', views.chapter, name='w.chapter'),
]