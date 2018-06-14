from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, Http404, redirect
from django.views import generic

from .forms import CommentForm, EditCommentForm
from .models import Comment
from posts.models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class CommentView(LoginRequiredMixin, generic.TemplateView):
    """
    User can comment on the detail view of each post
    """
    login_url = 'login'
    template_name = 'comment_thread.html'

    def get(self, *args, **kwargs):
        id = kwargs.get('id', None)
        users = Profile.objects.all()
        user = self.request.user
        instance = get_object_or_404(Comment, id=id)
        prof_instance = get_object_or_404(Profile, user=user)

        if not instance.is_parent:
            instance = instance.parent

        initial_data = {
            'content_type':instance.content_type,
            'object_id':instance.object_id,
        }

        form = CommentForm(
            self.request.POST or None, 
            initial=initial_data
        )

        context = {
            'comment': instance,
            'form':form,
            'prof_instance':prof_instance,
            'users':users,
        }
        return render(self.request, self.template_name, context)


    def post(self, *args, **kwargs):

        id = kwargs.get('id', None)
        user = self.request.user
        users = Profile.objects.all()
        instance = get_object_or_404(Comment, id=id)
        prof_instance = get_object_or_404(Profile, user=user)

        if not instance.is_parent:
            instance = instance.parent


        initial_data = {
            'content_type':instance.content_type,
            'object_id':instance.object_id,
        }

        form = CommentForm(
            self.request.POST or None, 
            initial=initial_data
        )

        if form.is_valid():
           new_comment = form.save(user=user)
           return HttpResponseRedirect(new_comment.get_absolute_url())

        context = {
            'comment': instance,
            'form':form,
            'prof_instance':prof_instance,
            'users':users,
        }
        return render(self.request, self.template_name, context)


class CommentDeleteView(LoginRequiredMixin, generic.TemplateView):
    """
    User can delete his/her own comments
    """
    login_url = 'login'
    template_name = 'confirm_delete.html'

    def get(self, *args, **kwargs):
        id = kwargs.get('id', None)
        user = self.request.user
        users = Profile.objects.all()
        prof_instance = get_object_or_404(Profile, user=user)

        try:
            instance = Comment.objects.get(id=id)
        except:
            raise Http404

        if self.request.user != instance.author:
            raise Http404

        context = {
            'instance':instance,
            'prof_instance':prof_instance,
            'users':users,
        }

        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        id = kwargs.get('id', None)
        user = self.request.user
        users = Profile.objects.all()
        prof_instance = get_object_or_404(Profile, user=user)


        try:
            instance = Comment.objects.get(id=id)
        except:
            raise Http404

        if self.request.user != instance.author:
            raise Http404

        if self.request.method == 'POST':
            parent_instance_url = instance.content_object.get_absolute_url()
            instance.delete()
            return HttpResponseRedirect(parent_instance_url)

        context = {
            'instance':instance,
            'prof_instance':prof_instance,
            'users':users,
        }

        return render(self.request, self.template_name, context)



class CommentEditView(LoginRequiredMixin, generic.TemplateView):
    """
    User can edit his/her own comments
    """
    login_url = 'login'
    template_name = 'post_form.html'
    title = 'Edit Comment'

    def get(self, *args, **kwargs):
        title = 'Edit Comment'
        id = kwargs.get('id', None)
        user = self.request.user
        users = Profile.objects.all()
        instance = get_object_or_404(Comment, id=id)
        prof_instance = get_object_or_404(Profile, user=user)

        initial_data = {
            'content':instance.content,
        }
        
        form = EditCommentForm(
            self.request.POST or None,
            initial=initial_data,
        )

        context = {
            'title':title,
            'instance': instance,
            'prof_instance':prof_instance,
            'form':form,
            'users':users,
        }
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        title = 'Edit Comment'
        id = kwargs.get('id', None)
        user = self.request.user
        users = Profile.objects.all()
        instance = get_object_or_404(Comment, id=id)
        prof_instance = get_object_or_404(Profile, user=user)

        initial_data = {
            'content':instance.content,
        }

        form = EditCommentForm(
            self.request.POST or None, 
            initial=initial_data,
        )

        if form.is_valid():
            form.save(id=id)
            return HttpResponseRedirect(instance.content_object.get_absolute_url())

        context = {
            'title':title,
            'instance': instance,
            'prof_instance':prof_instance,
            'form':form,
            'users':users,
        }

        return render(self.request, self.template_name, context)
