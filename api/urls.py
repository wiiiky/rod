# encoding=utf-8

from django.urls import path
from api import views

urlpatterns = [
    path('novels', views.novels, name='api.novels'),
    path('novel/<slug:npk>/chapters', views.novel_chapters, name='api.novel_chapters'),
    path('chapter/<slug:pk>', views.chapter, name='api.chapter'),
]
