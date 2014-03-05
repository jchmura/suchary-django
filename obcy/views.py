from django.shortcuts import render
from django.template import RequestContext

from obcy.extras import prepare_view


def all_sites(request):
    context = prepare_view.all_sites(request)
    return render(request, "obce_all.html", context, context_instance=RequestContext(request))


def one_joke(request, jokeslug):
    context = prepare_view.one_joke(jokeslug)
    return render(request, 'obce_one.html', context, context_instance=RequestContext(request))


def test(request):
    context = prepare_view.all_sites(request)
    return render(request, "test.html", context, context_instance=RequestContext(request))