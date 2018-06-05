from django.db import models
from django.conf import settings
from django.urls import reverse


# Create your models here.

def upload_location(instance, filename):
	return "%s/%s" %(instance.id, filename)


class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, default=1)
	bio = models.CharField(max_length=100)
	prof_pic = models.ImageField(upload_to=upload_location, 
		null=True, 
		blank=True)

	def __str__(self):
		return self.user.username

class Post(models.Model):
	author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, default=1)
	image = models.ImageField(upload_to=upload_location, 
		null=True, 
		blank=True)
	content = models.CharField(max_length=200)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	created = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __str__(self):
		return self.content


	def get_absolute_url(self):
		return reverse('posts:detail', kwargs={ 'id':self.id })

	class Meta:
		ordering = ["-created"]


