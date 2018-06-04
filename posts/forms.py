from django import forms
from .models import Post, Profile

class PostForm(forms.ModelForm):
	
	class Meta:
		model = Post
		fields = [
			"image",
			"content",
		]


class ProfileForm(forms.ModelForm):
	
	class Meta:
		model = Profile
		fields = [
			"bio",
			"prof_pic",
		]