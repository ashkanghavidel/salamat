from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def lookup(d, key):
    return d[key]
