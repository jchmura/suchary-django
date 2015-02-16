from django import template


register = template.Library()


@register.filter(name='lookup')
def cut(value, arg):
    return value[arg]


@register.filter(name='lt')
def lt(a, b):
    return a < b

@register.filter(name='sub')
def sub(a, b):
    return a - b
