from urllib.parse import quote

from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.views import generic
from django.urls import reverse

from comments.forms import CommentForm
from comments.models import Comment
from .models import Post, Profile
from .forms import PostForm, EditProfileForm, EditPasswordForm, EditProfPicForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class CreateView(LoginRequiredMixin, generic.TemplateView):
    login_url = 'login'
    template_name = 'post_form.html'

    def get(self, *args, **kwargs):
        title = 'Create Post'
        user = self.request.user
        users = Profile.objects.all()
        prof_instance = get_object_or_404(Profile, user=user)

        form = PostForm(
            self.request.POST or None, 
            self.request.FILES or None
        )

        context = {
            'title':title,
            'form': form,
            'users':users,
            'prof_instance':prof_instance,
        }
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        title = 'Create Post'
        user = self.request.user
        users = Profile.objects.all()
        prof_instance = get_object_or_404(Profile, user=user)

        form = PostForm(
            self.request.POST or None, 
            self.request.FILES or None
        )

        if form.is_valid():
            instance = Post()
            instance.image = self.request.FILES.get('image')
            instance.content = self.request.POST['content']
            instance.author = self.request.user
            instance.save()
            return HttpResponseRedirect('/')
        context = {
            'title':title,
            'form': form,
            'users':users,
            'prof_instance':prof_instance,
        }
        return render(self.request, self.template_name, context)


class ListView(LoginRequiredMixin, generic.ListView):
    login_url = 'login'
    template_name = 'post_list.html'

    def get(self, *args, **kwargs):
        user = self.request.user
        instance = get_object_or_404(Profile, user=user)

        queryset_list = Post.objects.all()
        users = Profile.objects.all()

        error = False
        if 'q' in self.request.GET:
            query = self.request.GET.get('q')

            if query:
                queryset_list = queryset_list.filter(
                    Q(content__icontains=query) |
                    Q(author__username__icontains=query) |
                    Q(author__first_name__icontains=query) |
                    Q(author__last_name__icontains=query)

                ).distinct()

            elif not query:
                error = True

        paginator = Paginator(queryset_list, 3)
        page_request_var = 'page'
        page = self.request.GET.get(page_request_var)
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)

        context = {
            'object_list':queryset,
            'page_request_var': page_request_var,
            'instance':instance,
            'prof_instance':instance,
            'users':users,
            'error':error,
        }

        return render(self.request,self.template_name,context)

class DetailView(LoginRequiredMixin, generic.DetailView):
    login_url = 'login'
    template_name = 'post_detail.html'

    def get(self, *args, **kwargs):
        id = kwargs.get('id', None)
        instance = get_object_or_404(Post, id=id)
        users = Profile.objects.all()
        user = self.request.user
        prof_instance = get_object_or_404(Profile, user=user)


        initial_data = {
            'content_type':instance.get_content_type,
            'object_id':instance.id,
        }

        form = CommentForm(
            self.request.POST or None, 
            initial=initial_data
        )


        comments = instance.comments
        context = {
            'instance': instance,
            'comments':comments,
            'comment_form':form,
            'users':users,
            'prof_instance':prof_instance,
        }

        return render(self.request, self.template_name, context)


    def post(self, *args, **kwargs):
        id = kwargs.get('id', None)
        instance = get_object_or_404(Post, id=id)

        user = self.request.user
        users = Profile.objects.all()
        prof_instance = get_object_or_404(Profile, user=user)

        initial_data = {
            'content_type':instance.get_content_type,
            'object_id':instance.id,
        }

        form = CommentForm(
            self.request.POST or None, 
            initial=initial_data
        )

        if form.is_valid():
            c_type = form.cleaned_data.get('content_type')
            content_type = ContentType.objects.get(model=c_type)
            obj_id = form.cleaned_data.get('object_id')
            content_data = form.cleaned_data.get('content')
            parent_obj = None
            try:
                parent_id = self.request.POST.get('parent_id')
            except:
                parent_id = None

            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() == 1:
                    parent_obj = parent_qs.first()

            new_comment, created = Comment.objects.get_or_create(
                author = self.request.user,
                content_type = content_type,
                object_id = obj_id,
                content = content_data,
                parent = parent_obj,        
            )
            return HttpResponseRedirect(new_comment.content_object.get_absolute_url())


        comments = instance.comments

        context = {
            'instance': instance,
            'comments':comments,
            'comment_form':form,
            'users':users,
            'prof_instance':prof_instance,
        }

        return render(self.request, self.template_name, context)


class UpdateView(LoginRequiredMixin, generic.TemplateView):
    login_url = 'login'
    template_name = 'post_form.html'

    def get(self, *args, **kwargs):
        title = 'Update'
        id = kwargs.get('id', None)
        instance = get_object_or_404(Post, id=id)
        
        user = self.request.user
        users = Profile.objects.all()
        prof_instance = get_object_or_404(Profile, user=user)
        if self.request.user == instance.author:

            initial_data = {
                'image':instance.image,
                'content':instance.content
            }

            form = PostForm(
                self.request.POST or None, 
                self.request.FILES or None, 
                initial=initial_data
            )

        else:
            raise Http404
        context = {
            'title':title,
            'instance': instance,
            'form':form,
            'users':users,
            'prof_instance':prof_instance
        }
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        id = kwargs.get('id', None)
        instance = get_object_or_404(Post, id=id)
        if self.request.user == instance.author:

            initial_data = {
                'image':instance.image,
                'content':instance.content
            }

            form = PostForm(
                self.request.POST or None, 
                self.request.FILES or None, 
                initial=initial_data
            )

        if form.is_valid():
            if self.request.FILES.get('image'):
                instance.image = self.request.FILES.get('image')
            instance.content = self.request.POST['content']
            instance.save()
            return HttpResponseRedirect(instance.get_absolute_url())
        else:
            raise Http404

        context = {
            'title':title,
            'instance': instance,
            'form':form,
        }

        return render(self.request, self.template_name, context)


class DeleteView(LoginRequiredMixin, generic.TemplateView):
    login_url = 'login'
    template_name = 'confirm_delete.html'
    def get(self, *args, **kwargs):
        id = kwargs.get('id', None)
        instance = get_object_or_404(Post, id=id)
        user = self.request.user
        prof_instance = get_object_or_404(Profile, user=user)

        try:
            instance = Post.objects.get(id=id)
        except:
            raise Http404

        if self.request.user != instance.author:
            raise Http404

        context = {
            'instance':instance,
            'prof_instance':prof_instance,
        }

        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        id = kwargs.get('id', None)
        user = self.request.user
        prof_instance = get_object_or_404(Profile, user=user)


        try:
            instance = Post.objects.get(id=id)
        except:
            raise Http404

        if self.request.user != instance.author:
            raise Http404

        if self.request.method == 'POST':
            instance.delete()
            return HttpResponseRedirect(reverse ('posts:list'))

        context = {
            'instance':instance,
            'prof_instance':prof_instance,
        }

        return render(self.request, self.template_name, context)

class AboutView(generic.TemplateView):
	template_name = 'post_about.html'



class ProfileView(LoginRequiredMixin, generic.TemplateView):
    login_url = 'login'
    template_name = 'profile.html'

    def get(self, *args, **kwargs):


        users = Profile.objects.all()

        user = self.request.user
        instance = get_object_or_404(Profile, user=user)

        queryset = Post.objects.all().filter(author=user)


        context = {
            'object_list':queryset,
            'instance':instance,
            'prof_instance':instance,
            'users':users,
        }

        return render(self.request,self.template_name,context)




class EditProfileView(LoginRequiredMixin, generic.TemplateView):
    login_url = 'login'
    template_name = 'post_form.html'

    def get(self, *args, **kwargs):
        title = 'Edit Profile'
        user = self.request.user
        users = Profile.objects.all()
        instance = get_object_or_404(Profile, user=user)

        initial_data = {
            'email':user.email,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'username':user.username,
            'bio':instance.bio,
        }

        form = EditProfileForm(
            self.request.POST or None, 
            self.request.FILES or None,
            initial=initial_data,
        )

        context = {
            'title':title,
            'instance': instance,
            'prof_instance':instance,
            'form':form,
            'users':users,
        }
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        title = 'Edit Profile'	
        user = self.request.user
        users = Profile.objects.all()
        instance = get_object_or_404(Profile, user=user)

        initial_data = {
            'email':user.email,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'username':user.username,
            'bio':instance.bio,
        }

        form = EditProfileForm(
            self.request.POST or None, 
            self.request.FILES or None,
            initial=initial_data,
        )

        if form.is_valid():
            user.email = self.request.POST['email']
            user.first_name = self.request.POST['first_name']
            user.last_name = self.request.POST['last_name']
            user.save()
            instance.bio = self.request.POST['bio']
            instance.save()
            return HttpResponseRedirect(reverse('posts:list'))

        context = {
        	'title':title,
            'instance': instance,
            'prof_instance':instance,
            'form':form,
            'users':users,
        }

        return render(self.request, self.template_name, context)

class EditPassword(LoginRequiredMixin, generic.TemplateView):
    login_url = 'login'
    template_name='post_form.html'

    def get(self, *args, **kwargs):
        title = 'Edit Password'
        user = self.request.user
        users = Profile.objects.all()
        instance = get_object_or_404(Profile, user=user)

        form = EditPasswordForm(
            self.request.POST or None
        )

        context = {
            'title':title,
            'form':form,
            'prof_instance':instance,
            'users':users,
        }

        return render(self.request, self.template_name, context)


    def post(self, *args, **kwargs):
        title = 'Edit Password'
        users = Profile.objects.all()
        user = self.request.user
        instance = get_object_or_404(Profile, user=user)

        form = EditPasswordForm(
            self.request.POST or None
        )

        if form.is_valid():
            user.password = self.request.POST['password']
            user.set_password(user.password)
            user.save()
            login(self.request, user)
            return HttpResponseRedirect(reverse('posts:list'))

        context = {
            'title':title,
            'form':form,
            'prof_instance':instance,
            'users':users,
        }

        return render(self.request, self.template_name, context)


class EditProfPic(LoginRequiredMixin, generic.TemplateView):
    login_url = 'login'
    template_name='post_form.html'

    def get(self, *args, **kwargs):
        title = 'Edit Profile Picture'
        user = self.request.user
        users = Profile.objects.all()
        instance = get_object_or_404(Profile, user=user)

        initial_data = {
            'prof_pic':instance.prof_pic,
        }

        form = EditProfPicForm(
            self.request.POST or None,
            initial=initial_data,
        )

        context = {
            'title':title,
            'form':form,
            'prof_instance':instance,
            'users':users,
        }

        return render(self.request, self.template_name, context)


    def post(self, *args, **kwargs):
        title = 'Edit Profile Picture'
        users = Profile.objects.all()
        user = self.request.user
        instance = get_object_or_404(Profile, user=user)

        initial_data = {
            'prof_pic':instance.prof_pic,
        }

        form = EditProfPicForm(
            self.request.POST or None,
            initial=initial_data,
        )

        if form.is_valid():
            if self.request.FILES.get('prof_pic'):
                    instance.prof_pic = self.request.FILES.get('prof_pic')
            instance.save()
            return HttpResponseRedirect(reverse('posts:list'))

        context = {
            'title':title,
            'form':form,
            'prof_instance':instance,
            'users':users,
        }

        return render(self.request, self.template_name, context)