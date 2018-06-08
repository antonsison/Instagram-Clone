from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, Http404
from django.views import generic

from .forms import CommentForm
from .models import Comment
from posts.models import Profile
# Create your views here.

class CommentView(generic.TemplateView):
    template_name = "comment_thread.html"

    def get(self, *args, **kwargs):
        id = kwargs.get('id', None)
        users = Profile.objects.all()
        user = self.request.user
        instance = get_object_or_404(Comment, id=id)
        prof_instance = get_object_or_404(Profile, user=user)

        if not instance.is_parent:
            instance = instance.parent

        initial_data = {
            "content_type":instance.content_type,
            "object_id":instance.object_id,
        }

        form = CommentForm(self.request.POST or None, initial=initial_data)

        context = {
            "comment": instance,
            "form":form,
            "prof_instance":prof_instance,
            "users":users,
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
            "content_type":instance.content_type,
            "object_id":instance.object_id,
        }
        form = CommentForm(self.request.POST or None, initial=initial_data)

        if form.is_valid():
            c_type = form.cleaned_data.get("content_type")
            content_type = ContentType.objects.get(model=c_type)
            obj_id = form.cleaned_data.get("object_id")
            content_data = form.cleaned_data.get("content")
            parent_obj = None
            try:
                parent_id = self.request.POST.get("parent_id")
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

        context = {
            "comment": instance,
            "form":form,
            "prof_instance":prof_instance,
            "users":users,
        }
        return render(self.request, self.template_name, context)


class CommentDeleteView(generic.TemplateView):
    template_name = "confirm_delete.html"

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
            "instance":instance,
            "prof_instance":prof_instance,
            "users":users,
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

        if self.request.method == "POST":
            parent_instance_url = instance.content_object.get_absolute_url()
            instance.delete()
            return HttpResponseRedirect(parent_instance_url)

        context = {
            "instance":instance,
            "prof_instance":prof_instance,
            "users":users,
        }

        return render(self.request, self.template_name, context)



class CommentEditView(generic.TemplateView):
    template_name = "post_form.html"
    title = "Edit Comment"

    def get(self, *args, **kwargs):
        title = "Edit Comment"
        id = kwargs.get('id', None)
        user = self.request.user
        users = Profile.objects.all()
        instance = get_object_or_404(Comment, id=id)
        prof_instance = get_object_or_404(Profile, user=user)

        info = {
            "content":instance.content
        }
        
        form = CommentForm(
            self.request.POST or None,
            initial=info,
        )

        context = {
            "title":title,
            "instance": instance,
            "prof_instance":prof_instance,
            "form":form,
            "users":users,
        }
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        title = "Edit Comment"
        id = kwargs.get('id', None)
        user = self.request.user
        users = Profile.objects.all()
        instance = get_object_or_404(Comment, id=id)
        prof_instance = get_object_or_404(Profile, user=user)

        info = {
            "content":instance.content
        }

        form = CommentForm(
            self.request.POST or None, 
            initial=info,
        )

        if form.is_valid():
            instance.content = self.request.POST['content']
            instance.save()
            return HttpResponseRedirect(instance.content_object.get_absolute_url())

        context = {
            "title":title,
            "instance": instance,
            "prof_instance":prof_instance,
            "form":form,
            "users":users,
        }

        return render(self.request, self.template_name, context)
