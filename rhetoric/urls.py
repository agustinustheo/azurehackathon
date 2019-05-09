from django.urls import path
from . import views
from django.views.generic import ListView, DetailView
from django.conf.urls import url, include

urlpatterns = [
    path('', views.home, name="judgeyou-rhetoric-home"),
    path('upload', views.upload, name="judgeyou-rhetoric-upload"),
]
