import json
import logging

from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from django.views.decorators.http import require_POST

from obcy.extras import prepare_view
from obcy.models import Joke
from api.commands import edit_joke as api_edit_joke
from api.commands import delete_joke as api_remove_joke


logger = logging.getLogger(__name__)


def all_sites(request):
    context = prepare_view.all_sites(request)
    return render(request, "obce_all.html", context, context_instance=RequestContext(request))


def one_joke(request, jokeslug):
    context = prepare_view.one_joke(request, jokeslug)
    return render(request, 'obce_one.html', context, context_instance=RequestContext(request))


def all_random(request):
    context = prepare_view.random(request)
    return render(request, 'obce_all.html', context, context_instance=RequestContext(request))


@require_POST
def edit_joke(request, pk):
    body = request.POST.get('body', '')
    if not body:
        return HttpResponse(status=400)

    user = request.user.groups.filter(name='Moderator')
    if user:
        joke = Joke.objects.get(pk=pk)
        joke.body = body
        joke.save()
        logger.info('Joke %s edited.', joke.key)
        api_edit_joke(joke.key)
        return HttpResponse(status=200)
    else:
        return HttpResponse('User not authorised to edit joke')


@require_POST
def delete_joke(request, pk):
    user = request.user.groups.filter(name='Moderator')
    if user:
        joke = Joke.objects.get(pk=pk)
        joke.hidden = True
        joke.save()
        logger.info('Joke %s removed.', joke.key)
        api_remove_joke(joke.key)
        return HttpResponse(status=200)
    else:
        return HttpResponse('User not authorised to remove joke')


def json_response(data=None, status_code=200):
    if data is None:
        data = ''
    return HttpResponse(json.dumps(data), content_type='application/json', status=status_code)