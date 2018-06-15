from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType

from comments.models import Comment

User = settings.AUTH_USER_MODEL
# Create your models here.

def upload_location(instance, filename):
	return "%s/%s" %(instance.id, filename)


class Profile(models.Model):
	user = models.OneToOneField(
		User,
		on_delete=models.CASCADE, 
		default=1
	)
	bio = models.CharField(max_length=100)
	followers = models.ManyToManyField(User, related_name='is_following', blank=True, symmetrical=False)
	prof_pic = models.ImageField(
		upload_to=upload_location,
		null=True, 
		blank=True,
	)

	def __str__(self):
		return self.user.username

class Post(models.Model):
	author = models.ForeignKey(
		User,
		on_delete=models.CASCADE, 
		default=1
	)

	image = models.ImageField(
		upload_to=upload_location,
		null=True, 
		blank=True)

	content = models.CharField(max_length=200)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	created = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __str__(self):
		return self.content


	def get_absolute_url(self):
		return reverse('posts:detail', kwargs={ 'id':self.id })

	def get_delete_url(self):
		return reverse("posts:delete", kwargs={"id": self.id})

	def get_profile_url(self):
		return reverse('posts:profile', kwargs={ 'user':self.user.username })

	class Meta:
		ordering = ["-created"]

	@property
	def comments(self):
		instance = self
		qs = Comment.objects.filter_by_instance(instance)
		return qs

	@property
	def get_content_type(self):
		instance = self
		content_type = ContentType.objects.get_for_model(instance.__class__)
		return content_type


