from django import forms
from .models import Post, Profile

from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
	
	class Meta:
		model = Post
		fields = [
			"image",
			"content",
		]

class EditProfileForm(forms.Form):
	email = forms.EmailField(label='Email Address')
	first_name = forms.CharField(max_length=20)
	last_name = forms.CharField(max_length=20)
	bio = forms.CharField(max_length=200, required=False)


	# def clean_email(self):
	# 	email = self.cleaned_data.get('email')
	# 	email_qs = User.objects.filter(email=email)
	# 	if email_qs.exists():
	# 		raise forms.ValidationError("This email has already been registered")


class EditPasswordForm(forms.Form):
	password  = forms.CharField(label="Password", widget=forms.PasswordInput)
	password2  = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

	# class Meta:
	# 	model = User
	# 	fields = [
	# 		"password"
	# 		"password2"
	# 	]

	def clean_password2(self):
		password = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password2')
		if password2 != password:
			raise forms.ValidationError("Passwords must match")


class EditProfPicForm(forms.Form):
	prof_pic = forms.ImageField(label='Profile Picture', required=False)