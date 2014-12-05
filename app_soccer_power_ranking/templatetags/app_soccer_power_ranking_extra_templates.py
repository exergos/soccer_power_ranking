# This template tag makes sure you can access lists per index in html template
from django import template

register = template.Library()

@register.filter
def get_at_index(list, index):
    return list[index]