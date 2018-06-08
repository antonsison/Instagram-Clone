from django.urls import path, re_path
from .views import ListView, CreateView, AboutView, DetailView, UpdateView, DeleteView, ProfileView, EditProfileView, EditPassword
from . import views
from . models import Profile

app_name = "posts"

urlpatterns = [
	path('', views.ListView.as_view(), name='list'),
	path('create/', views.CreateView.as_view(), name='create'),
	path('about/', views.AboutView.as_view(), name='about'),
    path('password/edit', views.EditPassword.as_view(), name='edit_password'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
	path('profile/edit/', views.EditProfileView.as_view(), name='edit_profile'),
    re_path(r'^profile/(?P<user>[\w.@+-]+)/$', views.ProfileView.as_view(), name='profile_with_user'),
	re_path(r'^(?P<id>\d+)/$', views.DetailView.as_view(), name='detail'),
	re_path(r'^(?P<id>\d+)/edit/$', views.UpdateView.as_view(), name='update'),
	re_path(r'^(?P<id>\d+)/delete/$', views.DeleteView.as_view(), name='delete'),

]