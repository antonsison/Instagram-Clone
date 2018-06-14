from django import forms
from .models import Comment
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

class CommentForm(forms.Form):
    """
    Form for the comment
    """
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    content = forms.CharField(label='', widget=forms.Textarea)


    def save(self, user=None):
        data = self.cleaned_data
        c_type = data.get('content_type')
        content_type = ContentType.objects.get(model=c_type)
        obj_id = data.get('object_id')
        content_data = data.get('content')
        parent_obj = None
        try:
            parent_id = data.get('parent_id')
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
            author = user,
            content_type = content_type,
            object_id = obj_id,
            content = content_data,
            parent = parent_obj,        
        )
        # import pdb; pdb.set_trace()
        return new_comment.content_object

class EditCommentForm(forms.Form):
    """
    Form for the edit comment
    """
    content = forms.CharField(label='', widget=forms.Textarea)


    def save(self, id=None):
        data = self.cleaned_data

        content = data.get('content')

        instance = get_object_or_404(Comment, id=id)
        instance.content = content
        instance.save()