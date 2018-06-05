from urllib.parse import quote

from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.utils import timezone
from django.views import generic

from comments.models import Comment
from .models import Post, Profile
from .forms import PostForm
from registration.forms import UserRegisterForm

from django.contrib.auth import (
	authenticate,
	login,
	logout,
)


# Create your views here.

class CreateView(generic.TemplateView):
	template_name = "post_form.html"

	def get(self, *args, **kwargs):
		title= "Create"
		if self.request.user.is_authenticated:
			form = PostForm(
                self.request.POST or None, 
                self.request.FILES or None
            )
		else:
			raise Http404

		context = {
		"title":title,
		"form": form,
		}
		return render(self.request, self.template_name, context)

	def post(self, *args, **kwargs):
		if self.request.user.is_authenticated:
			form = PostForm(
                self.request.POST or None, 
                self.request.FILES or None
            )

			if form.is_valid():
				instance = form.save(commit=False)
				instance.author = self.request.user
				instance.save()
				return HttpResponseRedirect("/")
		else:
			raise Http404
		context = {
		"title":title,
		"instance": instance,
		"form": form,
		}
		return render(self.request, self.template_name, context)


class ListView(generic.ListView):
	template_name = "post_list.html"

	def get(self, *args, **kwargs):
		if self.request.user.is_authenticated:

			user = self.request.user
			instance = get_object_or_404(Profile, user=user)

			queryset_list = Post.objects.all()

			query = self.request.GET.get("q")
			if query:
				queryset_list = queryset_list.filter(
					Q(content__icontains=query) |
					Q(author__username__icontains=query) |
					Q(author__first_name__icontains=query) |
					Q(author__last_name__icontains=query)

					).distinct()
			paginator = Paginator(queryset_list, 3)
			page_request_var = 'page'
			page = self.request.GET.get(page_request_var)
			try:
				queryset = paginator.page(page)
			except PageNotAnInteger:
				queryset = paginator.page(1)
			except EmptyPage:
				queryset = paginator.page(paginator.num_pages)

		else:
			return redirect("login")

		context = {
			"object_list":queryset,
			"page_request_var": page_request_var,
			"instance":instance,
		}

		return render(self.request,self.template_name,context)

class DetailView(generic.DetailView):
    template_name = "post_detail.html"

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            id = kwargs.get('id', None)
            instance = get_object_or_404(Post, id=id)
        else:
            return redirect("login")

        content_type = ContentType.objects.get_for_model(Post)
        obj_id = instance.id
        # Post.objects.get(id=instance.id)
        comments = Comment.objects.filter(
        content_type=content_type, 
        object_id=obj_id
        )

        context = {
        "instance": instance,
        "comments":comments
        }

        return render(self.request, self.template_name, context)


class UpdateView(generic.TemplateView):
    template_name = "post_form.html"

    def get(self, *args, **kwargs):
        title = "Update"
        id = kwargs.get('id', None)
        instance = get_object_or_404(Post, id=id)
        if self.request.user.is_authenticated and self.request.user == instance.author:

            form = PostForm(
            self.request.POST or None, 
            self.request.FILES or None, 
            instance=instance
            )

        else:
            raise Http404
        context = {
        "title":title,
        "instance": instance,
        "form":form,
        }
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        id = kwargs.get('id', None)
        instance = get_object_or_404(Post, id=id)
        if self.request.user.is_authenticated and self.request.user == instance.author:
            form = PostForm(
            self.request.POST or None, 
            self.request.FILES or None, 
            instance=instance
            )

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return HttpResponseRedirect(instance.get_absolute_url())
        else:
            raise Http404

        context = {
        "title":title,
        "instance": instance,
        "form":form,
        }

        return render(self.request, self.template_name, context)


class DeleteView(generic.TemplateView):
    template_name = "/"

    def get(self, *args, **kwargs):
        id = kwargs.get('id', None)
        instance = get_object_or_404(Post, id=id)
        if self.request.user.is_authenticated and self.request.user == instance.author:
            instance.delete()
            return redirect(self.template_name)
        else:
            raise Http404

class AboutView(generic.TemplateView):
	template_name = "post_about.html"



class ProfileView(generic.TemplateView):
	template_name = "profile.html"

	def get(self, *args, **kwargs):
		if self.request.user.is_authenticated:
			user = self.request.user
			instance = get_object_or_404(Profile, user=user)

			queryset_list = Post.objects.all().filter(author=user)

			query = self.request.GET.get("q")
			if query:
				queryset_list = queryset_list.filter(
                    Q(content__icontains=query)
                ).distinct()
			paginator = Paginator(queryset_list, 3)
			page_request_var = 'page'
			page = self.request.GET.get(page_request_var)
			try:
				queryset = paginator.page(page)
			except PageNotAnInteger:
				queryset = paginator.page(1)
			except EmptyPage:
				queryset = paginator.page(paginator.num_pages)

		else:
			return redirect("login")

		context = {
			"object_list":queryset,
			"page_request_var": page_request_var,
			"instance":instance,
		}

		return render(self.request,self.template_name,context)


class EditProfileView(generic.TemplateView):
    template_name = 'post_form.html'

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
             title = "Edit Profile"
             user = self.request.user
             instance = get_object_or_404(Profile, user=user)

             form = UserRegisterForm(
                self.request.POST or None, 
                self.request.FILES or None, 
            )
        else:
            raise Http404
        context = {
            "title":title,
            "instance": instance,
            "form":form,
        }
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            title = "Edit Profile"	
            user = self.request.user
            instance = get_object_or_404(Profile, user=user)
            form = UserRegisterForm(
                self.request.POST or None, 
                self.request.FILES or None, 
            )

            if form.is_valid():
                user.email = self.request.POST['email']
                user.first_name = self.request.POST['first_name']
                user.last_name = self.request.POST['last_name']
                user.username = self.request.POST['username']
                user.password = self.request.POST['password']
                user.set_password(user.password)
                user.save()
                instance.bio = self.request.POST['bio']
                if self.request.FILES['prof_pic']:
                    instance.prof_pic = self.request.FILES['prof_pic']
                instance.save()
                return redirect("/")
        else:
            raise Http404

        context = {
        	"title":title,
            "instance": instance,
            "form":form,
        }

        return render(self.request, self.template_name, context)









