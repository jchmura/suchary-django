from copy import copy

from django import template


register = template.Library()


@register.inclusion_tag('joke.html', takes_context=True)
def display_joke(context, joke_obj):
    context = copy(context)
    context.update({'joke': joke_obj})
    return context