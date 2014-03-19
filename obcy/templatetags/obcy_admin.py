from django import template

register = template.Library()


@register.inclusion_tag('admin/obcy_mod.html', takes_context=True)
def mod_joke(context, pk):
    return {'joke_id': pk, 'moderator': context['moderator']}


@register.inclusion_tag('admin/obcy_mod_js.html', takes_context=True)
def mod_joke_js(context):
    return {'moderator': context['moderator']}