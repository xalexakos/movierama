from django import template
from django.template.defaultfilters import safe

register = template.Library()


@register.simple_tag
def get_user_repr(request, user):
    return safe('<a href="/?user=%(user_id)s">%(user_repr)s</a>' % {'user_id': user.id, 'user_repr': '%s' % user})


@register.filter()
def pages_range(max_page):
    return range(1, max_page + 1)
