# encoding=utf-8

from django.conf.urls import url, include
from web import views

urlpatterns = [
    url(r'^$', views.index),
]
