# encoding=utf-8

from django.conf.urls import url, include
from writer import views

urlpatterns = [
    url(r'^$', views.index, name='w.index'),
    url(r'^login/?$', views.login, name='w.login'),
]
