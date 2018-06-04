from django import forms
from django.conf import settings
from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
)

User = get_user_model()

class UserLoginForm(forms.Form):
	username = forms.CharField(max_length=20)
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")

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

class UserRegisterForm(forms.ModelForm):
	email = forms.EmailField(label='Email Address')
	first_name = forms.CharField(max_length=20)
	last_name = forms.CharField(max_length=20)
	username = forms.CharField(max_length=20)
	password  = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = [
			"email",
			"first_name",
			"last_name",
			"username",
			"password",
			
		]

	def clean(self):
		username = self.cleaned_data.get('username')
		username_qs = User.objects.filter(username=username)
		if username_qs.exists():
			raise forms.ValidationError("This username has already been used")

		email = self.cleaned_data.get('email')
		email_qs = User.objects.filter(email=email)
		if email_qs.exists():
			raise forms.ValidationError("This email has already been registered")