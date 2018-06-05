from django import forms
from .models import Post, Profile

from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
)

User = get_user_model()

class PostForm(forms.ModelForm):
	
	class Meta:
		model = Post
		fields = [
			"image",
			"content",
		]
