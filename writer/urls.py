# encoding=utf-8

from django.urls import path
from writer import views

urlpatterns = [
    path('', views.index, name='w.index'),
    path('login', views.login, name='w.login'),
    path('logout', views.logout, name='w.logout'),
    path('profile', views.profile, name='w.profile'),
    path('settings', views.settings, name='w.settings'),
    path('n/<slug:pk>', views.novel, name='w.novel'),
    path('n/<slug:pk>/c/<slug:cpk>', views.chapter, name='w.chapter'),
    path('image', views.upload_image, name='image-upload'),
]
