# encoding=utf-8

from django.urls import path
from web import views

urlpatterns = [
    path('', views.index, name='index'),
    path('n/<slug:pk>', views.novel, name='novel'),
    path('n/<slug:pk>/c/<slug:cpk>', views.chapter, name='chapter'),
    path('n/<slug:pk>/c/<slug:cpk>/comment',
         views.chapter_comment, name='chapter.comment'),
    path('copyright', views.copyright, name='copyright'),
    path('about', views.about, name='about'),
]
