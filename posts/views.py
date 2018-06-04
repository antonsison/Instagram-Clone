from urllib.parse import quote

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.utils import timezone
from django.views import generic

from .models import Post, Profile
from .forms import PostForm, ProfileForm

from registration.views import LoginView, RegisterView, LogoutView

# Create your views here.

class CreateView(generic.TemplateView):
	template_name = "post_form.html"

	def get(self, request):
		title= "Create"
		if request.user.is_authenticated:
			form = PostForm(request.POST or None, request.FILES or None)
		else:
			raise Http404

		context = {
		"title":title,
		"form": form,
		}
		return render(request, self.template_name, context)

	def post(self, request):
		if request.user.is_authenticated:
			form = PostForm(request.POST or None, request.FILES or None)
			if form.is_valid():
				instance = form.save(commit=False)
				instance.author = request.user
				instance.save()
				return HttpResponseRedirect("/")
		else:
			raise Http404
		context = {
		"instance": instance,
		"form": form,
		}
		return render(request, self.template_name, context)


class ListView(generic.ListView):
	template_name = "post_list.html"

	def get(self, request):
		if request.user.is_authenticated:

			user = self.request.user
			profile = get_object_or_404(Profile, user=user)

			queryset_list = Post.objects.all()

			query = request.GET.get("q")
			if query:
				queryset_list = queryset_list.filter(
					Q(content__icontains=query) |
					Q(author__username__icontains=query) |
					Q(author__first_name__icontains=query) |
					Q(author__last_name__icontains=query)

					).distinct()
			paginator = Paginator(queryset_list, 3)
			page_request_var = 'page'
			page = request.GET.get(page_request_var)
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
			"username":user.username,
			"first_name":user.first_name,
			"last_name":user.last_name,
			"prof_pic":profile.prof_pic,
			"bio": profile.bio,
		}

		return render(request,self.template_name,context)

class DetailView(generic.DetailView):
	template_name = "post_detail.html"

	def get(self, request, id=None):
		if request.user.is_authenticated:
			instance = get_object_or_404(Post, id=id)
		else:
			return redirect("login")

		context = {
		"instance": instance,
		}

		return render(request, self.template_name, context)


class UpdateView(generic.TemplateView):
	template_name = "post_form.html"

	def get(self, request, id=None):
		title = "Update"
		instance = get_object_or_404(Post, id=id)
		if request.user.is_authenticated and request.user == instance.author:
			
			form = PostForm(self.request.POST or None, self.request.FILES or None, instance=instance)
		else:
			raise Http404
		context = {
			"title":title,
			"instance": instance,
			"form":form,
		}
		return render(request, self.template_name, context)

	def post(self, request, id=None):
		instance = get_object_or_404(Post, id=id)
		if request.user.is_authenticated and request.user == instance.author:
			form = PostForm(self.request.POST or None, self.request.FILES or None, instance=instance)
			if form.is_valid():
				instance = form.save(commit=False)
				instance.save()
				return HttpResponseRedirect(instance.get_absolute_url())
		else:
			raise Http404
		context = {
			"instance": instance,
			"form":form,
		}

		return render(request, self.template_name, context)


class DeleteView(generic.TemplateView):
	template_name = "/"

	def get(self, request, id=None):
		instance = get_object_or_404(Post, id=id)
		if request.user.is_authenticated and request.user == instance.author:
			instance.delete()
			return redirect(self.template_name)
		else:
			raise Http404

class AboutView(generic.TemplateView):
	template_name = "post_about.html"



class ProfileView(generic.TemplateView):
	template_name = "profile.html"

	def get(self, request):
		if request.user.is_authenticated:

			user = self.request.user
			profile = get_object_or_404(Profile, user=user)

			queryset_list = Post.objects.all()

			query = request.GET.get("q")
			if query:
				queryset_list = queryset_list.filter(
					Q(content__icontains=query) |
					Q(author__username__icontains=query) |
					Q(author__first_name__icontains=query) |
					Q(author__last_name__icontains=query)

					).distinct()
			paginator = Paginator(queryset_list, 3)
			page_request_var = 'page'
			page = request.GET.get(page_request_var)
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
			"username":user.username,
			"first_name":user.first_name,
			"last_name":user.last_name,
			"prof_pic":profile.prof_pic,
			"bio": profile.bio,
		}

		return render(request,self.template_name,context)
