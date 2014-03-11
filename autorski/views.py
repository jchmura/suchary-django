from django.shortcuts import render
from django.template import RequestContext

from autorski.extras import prepare_view


def all_jokes(request):
    context = prepare_view.all_jokes(request)

    if request.user.is_authenticated():
        return all_jokes_logged(request, context)
    else:
        return all_jokes_not_logged(request, context)


def all_jokes_logged(request, context):
    return render(request, "autorski_all_logged.html", context, context_instance=RequestContext(request))


def all_jokes_not_logged(request, context):
    return render(request, "autorski_all_not_logged.html", context, context_instance=RequestContext(request))


def one_joke(request, jokeslug):
    context = prepare_view.one_joke(jokeslug)
    return render(request, 'autorski_one.html', context, context_instance=RequestContext(request))


def test(request):
    context = prepare_view.all_jokes(request)
    return render(request, "test.html", context, context_instance=RequestContext(request))