# encoding=utf-8

from django.conf.urls import url, include
from web import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^n/(?P<pk>\w+)$', views.novel, name='novel'),
    url(r'^n/(?P<pk>\w+)/c/(?P<cpk>\w+)$', views.chapter, name='chapter'),
    url(r'^n/(?P<pk>\w+)/c/(?P<cpk>\w+)/comment', views.chapter_comment, name='chapter.comment')
]
