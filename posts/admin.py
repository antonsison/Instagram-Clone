from django.contrib import admin
from .models import Post, Profile
# Register your models here.


class PostAdmin(admin.ModelAdmin):
	list_display = ["content", "created", "updated"]
	list_display_links = ["updated"]
	list_filter = ["created", "updated"]
	list_editable = ["content"]
	search_fields = ["author", "content"]


admin.site.register(Post, PostAdmin)
admin.site.register(Profile)