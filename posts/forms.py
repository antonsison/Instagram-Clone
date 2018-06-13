from django import forms
from .models import Post, Profile
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

class PostForm(forms.Form):
	"""
	Form for the post when a user creates a post
	"""
	image = forms.ImageField(required=False)
	content = forms.CharField(label='Caption', required=False)

	def save(self, user=None):
		data = self.cleaned_data
		instance = Post(
			image=data.get('image'),
			content=data['content'],
			author=user
		)
		# import pdb; pdb.set_trace()
		instance.save()

	def clean_image(self):
		image = self.cleaned_data.get('image')
		if image == None:
			raise forms.ValidationError('Post must have an image!')
		return image


class EditProfileForm(forms.Form):
	"""
	Form for the currently logged in user if he/she wants to edit
	his/her profile
	"""
	email = forms.EmailField(label='Email Address')
	first_name = forms.CharField(max_length=20)
	last_name = forms.CharField(max_length=20)
	bio = forms.CharField(max_length=200, required=False)


	def save(self, user=None):
		data = self.cleaned_data
		instance = get_object_or_404(Profile, user=user)


		user.email = data['email']
		user.first_name = data['first_name']
		user.last_name = data['last_name']
		user.save()
		instance.bio = data['bio']
		instance.save()


	
class EditPasswordForm(forms.Form):
	"""
	Form for the currently logged in user if he/she wants to edit
	his/her password
	"""
	password  = forms.CharField(label="Password", widget=forms.PasswordInput)
	password2  = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

	def save(self, user=None):
		data = self.cleaned_data
		user.password = data['password']
		user.set_password(user.password)
		user.save()


	def clean_password2(self):
		password = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password2')

		if password2 != password:
			raise forms.ValidationError('Passwords must match')


class EditProfPicForm(forms.Form):
	"""
	Form for the currently logged in user if he/she wants to edit
	his/her profile picture
	"""
	prof_pic = forms.ImageField(label='Profile Picture', required=False)

	def save(self, user=None):
		data = self.cleaned_data
		instance = get_object_or_404(Profile, user=user)


		instance.prof_pic = data.get('prof_pic')
		instance.save()
