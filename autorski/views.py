from django.shortcuts import render
from django.template import RequestContext

from autorski.extras import prepare_view


def all_jokes(request):
    context = prepare_view.all_jokes(request)
    return render(request, "autorski_all.html", context, context_instance=RequestContext(request))
