from django import template


register = template.Library()


@register.filter(name='upclass')
def compute_up_class(joke, user):
    if joke.upvotes.filter(username=user).count() > 0:
        return 'btn-success'
    else:
        return 'btn-default'


@register.filter(name='downclass')
def compute_down_class(joke, user):
    if joke.downvotes.filter(username=user).count() > 0:
        return 'btn-danger'
    else:
        return 'btn-default'


@register.filter(name='updisable')
def compute_up_disable(joke, user):
    if joke.upvotes.filter(username=user).count() > 0:
        return 'disabled=disabled'
    else:
        return ''


@register.filter(name='downdisable')
def compute_down_disable(joke, user):
    if joke.downvotes.filter(username=user).count() > 0:
        return 'disabled=disabled'
    else:
        return ''