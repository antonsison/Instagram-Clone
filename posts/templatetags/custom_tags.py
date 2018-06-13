from django import template
from ..models import Profile

register = template.Library()


@register.inclusion_tag('user_avatar.html')
def avatar(id=None):

    return {'id': Profile.objects.get(user_id=id), 'users':Profile.objects.all() }