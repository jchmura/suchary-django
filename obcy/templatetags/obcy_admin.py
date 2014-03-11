from django import template

register = template.Library()


@register.inclusion_tag('obcy_delete.html', takes_context=True)
def delete_joke(context, pk):
    return {'joke_id': pk, 'moderator': context['moderator']}


@register.inclusion_tag('obcy_delete_js.html', takes_context=True)
def delete_joke_js(context):
    return {'moderator': context['moderator']}