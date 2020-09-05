from django import template

register = template.Library()


@register.filter()
def pages_range(max_page):
    return range(1, max_page + 1)
