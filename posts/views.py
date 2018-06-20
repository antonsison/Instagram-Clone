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
from django.contrib.auth import login
from .forms import PostForm, EditProfileForm, EditPasswordForm, EditProfPicForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.http import JsonResponse


# Create your views here.

class CreateView(LoginRequiredMixin, generic.TemplateView):
    """
    Logged in user creates a new post
    """
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
            form.save(user=user)
            return HttpResponseRedirect('/')
        context = {
            'title':title,
            'form': form,
            'users':users,
            'prof_instance':prof_instance,
        }
        return render(self.request, self.template_name, context)


class ListView(LoginRequiredMixin, generic.ListView):
    """
    A list of the posts of all the users
    """
    login_url = 'login'
    template_name = 'post_list.html'

    def get(self, *args, **kwargs):
        user = self.request.user
        instance = get_object_or_404(Profile, user=user)

        is_following_user_ids = [x.user.id for x in user.is_following.all()]
        queryset_list = Post.objects.filter(
            Q(author__id__in=is_following_user_ids) |
            Q(author=user)
        )
        post_count = Post.objects.all().count()
        users = Profile.objects.all()

        error = False
        if 'q' in self.request.GET:
            query = self.request.GET.get('q')
            queryset_list = queryset_list.filter(
                    Q(content__icontains=query) |
                    Q(author__username__icontains=query) |
                    Q(author__first_name__icontains=query) |
                    Q(author__last_name__icontains=query)

                ).distinct()

            if not query:
                error = True
            elif query and queryset_list.count() == 0:
                error = True
            else:
                queryset_list
                


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
    """
    Sees the detail of a single post where users can comment
    """
    login_url = 'login'
    template_name = 'post_detail.html'

    def get(self, *args, **kwargs):
        id = kwargs.get('id', None)
        instance = get_object_or_404(Post, id=id)
        users = Profile.objects.all()
        user = self.request.user
        like = 'false'
        prof_instance = get_object_or_404(Profile, user=user)
        if user in instance.likes.all():
            like = 'true'


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
            'form':form,
            'users':users,
            'prof_instance':prof_instance,
            'like':like,
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
            new_comment = form.save(user=user)
            return HttpResponseRedirect(new_comment.get_absolute_url())


        comments = instance.comments

        context = {
            'instance': instance,
            'comments':comments,
            'form':form,
            'users':users,
            'prof_instance':prof_instance,
            'like':like,
        }

        return render(self.request, self.template_name, context)


class UpdateView(LoginRequiredMixin, generic.TemplateView):
    """
    Update view is basically the edit page for the posts
    where only the author of the post can edit his/her posts
    """
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
    """
    Delete view is when the author of a post wants to delete
    his/her post and redirects you to a confirmation page
    in case you change your mind on deleting the post
    """
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

class PostLikeToggle(LoginRequiredMixin, generic.View):
    """
    Logged in user can like or unlike own posts or other user's posts
    """
    login_url = 'login'

    def post(self, *args, **kwargs):
        id = kwargs.get('id', None)
        instance = get_object_or_404(Post, id=id)
        url = instance.get_absolute_url()
        user = self.request.user
        like = self.request.POST.get('liked')
        print(like, type(like))
        if like == 'true':
            instance.likes.remove(user)
            return JsonResponse({'liked':'true'})
        else:
            instance.likes.add(user)
            return JsonResponse({'liked':'false'})


class AboutView(generic.TemplateView):
	template_name = 'post_about.html'


class ProfileView(LoginRequiredMixin, generic.TemplateView):
    """
    View the profile of the currently logged in user
    """
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


class ProfileUserView(LoginRequiredMixin, generic.TemplateView):
    """
    View the profile of other users
    """
    login_url = 'login'
    template_name = 'profile.html'

    def get(self, *args, **kwargs):
        users = Profile.objects.all()
        id = kwargs.get('id', None)
        instance = get_object_or_404(Profile, user_id=id)
        queryset = Post.objects.all().filter(author_id=id)

        is_following = False
        if instance.user.profile in self.request.user.is_following.all():
            is_following = True


        context = {
            'object_list':queryset,
            'instance':instance,
            'prof_instance':instance,
            'users':users,
            'is_following':is_following,
        }

        return render(self.request,self.template_name,context)

class ProfileFollowToggle(LoginRequiredMixin, generic.View):
    """
    Logged in user can now follow other users to see their posts
    """
    login_url = 'login'
    def post(self, *args, **kwargs):
        # print(self.request.data)
        user_to_toggle = self.request.POST.get('username')
        profile = Profile.objects.get(user__username__iexact=user_to_toggle)
        user = self.request.user
        if user in profile.followers.all():
            profile.followers.remove(user)
        else:
            profile.followers.add(user)
        return redirect(f'/profile/{profile.user_id}/')


class ProfileFollowersView(LoginRequiredMixin, generic.TemplateView):
    """
    View the followers of the logged in user and other users
    """
    login_url = 'login'
    template_name = 'profile_followers.html'

    def get(self, *args, **kwargs):
        users = Profile.objects.all()
        id = kwargs.get('id', None)
        instance = get_object_or_404(Profile, user_id=id)

        is_following = False
        if instance.user.profile in self.request.user.is_following.all():
            is_following = True

        context = {
            'instance':instance,
            'prof_instance':instance,
            'users':users,
            'is_following':is_following,
        }

        return render(self.request,self.template_name,context)


class ProfileFollowingView(LoginRequiredMixin, generic.TemplateView):
    """
    View the users followed by logged in user and other users
    """
    login_url = 'login'
    template_name = 'profile_following.html'

    def get(self, *args, **kwargs):
        users = Profile.objects.all()
        id = kwargs.get('id', None)
        instance = get_object_or_404(Profile, user_id=id)

        is_following = False
        if instance.user.profile in self.request.user.is_following.all():
            is_following = True

        context = {
            'instance':instance,
            'prof_instance':instance,
            'users':users,
            'is_following':is_following,
        }

        return render(self.request,self.template_name,context)


class EditProfileView(LoginRequiredMixin, generic.TemplateView):
    """
    Edit the currently logged in user's profile
    """
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
        id = user.id
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
            initial=initial_data,
        )

        if form.is_valid():
            form.save(user=user)
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
    """
    Edit the currently logged in user's password
    """    
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
            form.save(user=user)
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
    """
    Edit the currently logged in user's profile picture
    """
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
            self.request.FILES or None,
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
            self.request.FILES or None,
            initial=initial_data,
        )

        if form.is_valid():
            form.save(user=user)
            return HttpResponseRedirect(reverse('posts:list'))

        context = {
            'title':title,
            'form':form,
            'prof_instance':instance,
            'users':users,
        }

        return render(self.request, self.template_name, context)