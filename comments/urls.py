from django.urls import path, re_path

from . import views

app_name = "comments"

urlpatterns = [
    re_path(r'^(?P<id>\d+)/$', views.CommentView.as_view(), name='thread'),
    re_path(r'^(?P<id>\d+)/delete/$', views.CommentDeleteView.as_view(), name='delete'),
    re_path(r'^(?P<id>\d+)/edit/$', views.CommentEditView.as_view(), name='edit'),
]