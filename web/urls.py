# encoding=utf-8

from django.conf.urls import url, include
from web import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^n/(?P<pk>\w+)$', views.novel, name='novel'),
    url(r'^n/(?P<pk>\w+)/c/(?P<seq>\d+)$', views.chapter, name='chapter'),
]
