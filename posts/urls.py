from django.urls import path, re_path
from .views import (
    ListView, CreateView, 
    AboutView, DetailView, 
    UpdateView, DeleteView, 
    ProfileView, ProfileUserView,
    EditProfileView, EditPassword, 
    EditProfPic, ProfileFollowToggle,
    PostLikeToggle, ProfileFollowersView,
    ProfileFollowingView,
)
from . import views
from . models import Profile

app_name = "posts"

urlpatterns = [
    path('', views.ListView.as_view(), name='list'),
    path('create/', views.CreateView.as_view(), name='create'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.EditProfileView.as_view(), name='edit_profile'),
    path('password/edit', views.EditPassword.as_view(), name='edit_password'),
    path('profile/picture/edit', views.EditProfPic.as_view(), name='edit_prof_pic'),
    path('profile/follow/', views.ProfileFollowToggle.as_view(), name='follow'),
    re_path(r'^(?P<id>\d+)/$', views.DetailView.as_view(), name='detail'),
    re_path(r'^(?P<id>\d+)/like/$', views.PostLikeToggle.as_view(), name='like'),
    re_path(r'^(?P<id>\d+)/edit/$', views.UpdateView.as_view(), name='update'),
    re_path(r'^(?P<id>\d+)/delete/$', views.DeleteView.as_view(), name='delete'),
    re_path(r'^profile/(?P<id>\d+)/$', views.ProfileUserView.as_view(), name='profile_with_user'),
    re_path(r'^profile/(?P<id>\d+)/followers/$', views.ProfileFollowersView.as_view(), name='profile_followers'),
    re_path(r'^profile/(?P<id>\d+)/following/$', views.ProfileFollowingView.as_view(), name='profile_following'),

]