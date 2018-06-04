from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
)
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .forms import UserLoginForm, UserRegisterForm
from posts.models import Profile

User = get_user_model()
# Create your tests here.


class LoginView(generic.TemplateView):
	template_name = "registration_form.html"

	def get_context_data(self, *args, **kwargs):
		context = super(LoginView, self).get_context_data(*args, **kwargs)
		title = "Login"
		form = UserLoginForm(self.request.POST or None)
		context.update({
			"title":title,
			"form":form,
		})
		return context


	def post(self, request):
		context = self.get_context_data()
		form = context.get('form')
		if form.is_valid():
			username = form.cleaned_data.get("username")
			password = form.cleaned_data.get("password")
			user_qs = User.objects.filter(username=username)
			if user_qs.count()==1:
				user = user_qs.first()
				login(request, user)
				return redirect("/")

		return render(request, self.template_name, context)


class RegisterView(generic.TemplateView):
	template_name = "registration_form.html"

	def get_context_data(self, *args, **kwargs):
		context = super(RegisterView, self).get_context_data(*args, **kwargs)
		title = "Register"
		form = UserRegisterForm(self.request.POST or None)
		context.update({
			"title":title,
			"form":form,
		})
		return context

	def post(self, request):
		context = self.get_context_data()
		form = context.get('form')
		if form.is_valid():
			user = form.save(commit=False)
			password = form.cleaned_data.get('password')
			user.set_password(password)
			user.save()
			return redirect("login")

		return render(request, self.template_name, context)


class LogoutView(generic.TemplateView):

	def get(self, request):
		logout(request)
		return redirect("login")
