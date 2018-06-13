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
	"""
	Display log in page where registered users can log in
	"""
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


	def post(self, *args, **kwargs):
		context = self.get_context_data()
		form = context.get('form')
		if form.is_valid():
			# form.save()
			data = form.cleaned_data
			username = data['username']
			password = data['password']
			user = authenticate(username=username, password=password)
			login(self.request, user)
			return redirect("/")

		return render(self.request, self.template_name, context)


class RegisterView(generic.TemplateView):
	"""
	Display register page where soon to be users 
	register to have their own account
	"""
	template_name = "registration_form.html"

	def get_context_data(self, *args, **kwargs):
		context = super(RegisterView, self).get_context_data(*args, **kwargs)
		title = "Register"
		form = UserRegisterForm(
			self.request.POST or None, 
			self.request.FILES or None
		)
		context.update({
			"title":title,
			"form":form,
		})
		return context

	def post(self, *args, **kwargs):
		context = self.get_context_data()
		form = context.get('form')
		if form.is_valid():
			user = form.save()
			login(self.request, user)
			return redirect("/")


		return render(self.request, self.template_name, context)


class LogoutView(generic.TemplateView):
	"""
	When a currently logged in user want to log out
	"""
	def get(self, request):
		logout(self.request)
		return redirect("login")




				