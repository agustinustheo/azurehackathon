from . import views
from django.urls import path
from rhetoric.models import Review
from django.conf.urls import url, include
from django.views.generic import ListView, DetailView

urlpatterns = [
    path('', views.home, name="judgeyou-rhetoric-home"),
    path('upload', views.upload, name="judgeyou-rhetoric-upload"),
    path('review', views.review, name="judgeyou-rhetoric-review"),
    path('pending', views.pending, name="judgeyou-rhetoric-post-review"),
    path('getCommentary', views.getCommentary, name="judgeyou-rhetoric-get-commentary"),
    path('commentary', ListView.as_view(queryset=Review.objects.all()[:10], template_name="rhetoric/commentary.html")),
    url(r'^commentating/(?P<yt_id>\w+)/$', views.commentating, name='judgeyou-rhetoric-post-review"'),
]