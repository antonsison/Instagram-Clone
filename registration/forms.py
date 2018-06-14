from django import forms
from django.conf import settings
from django.contrib.auth import (
	authenticate,
	login,
	logout,
)
from posts.models import Profile
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

class UserLoginForm(forms.Form):
	"""
	The form for the login page
	"""
	username = forms.CharField(max_length=20)
	password = forms.CharField(widget=forms.PasswordInput)

	def save(self):
		data = self.cleaned_data
		username = data['username']
		password = data['password']
		user = authenticate(username=username, password=password)

		return user


	def clean(self, *args, **kwargs):
		username = self.data.get("username")
		password = self.data.get("password")

		if username and password:
			user_qs = User.objects.filter(username=username)

			if user_qs.count()==1:
				user = user_qs.first()
			else:
				raise forms.ValidationError("This User Does Not Exist")

			if not user.check_password(password):
				raise forms.ValidationError("Incorrect Password")

			if not user.is_active:
				raise forms.ValidationError("This user is no longer active")

		return super(UserLoginForm, self).clean(*args, **kwargs)

class UserRegisterForm(forms.Form):
	"""
	The form for the register page
	"""
	email = forms.EmailField(label='Email Address')
	first_name = forms.CharField(max_length=20)
	last_name = forms.CharField(max_length=20)
	username = forms.CharField(max_length=20)
	password  = forms.CharField(widget=forms.PasswordInput)
	bio = forms.CharField(max_length=200, required=False)
	prof_pic = forms.ImageField(label='Profile Picture', required=False)

	def save(self):
		data = self.cleaned_data

		user = User(
			email = data['email'],
			first_name = data['first_name'],
			last_name = data['last_name'],
			username = data['username'],
			password = data['password'],
		)
		user.set_password(user.password)
		user.save()

		instance = Profile(
			user=user, 
			bio=data['bio'], 
			prof_pic=data['prof_pic']
		)
		instance.save()

		return user

	def clean_username(self):
		username = self.data.get('username')
		username_qs = User.objects.filter(username=username)
		if username_qs.exists():
			raise forms.ValidationError("This username has already been used")

		return username

