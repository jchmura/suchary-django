import logging

from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import RequestContext
from django.utils import timezone
from django.views.decorators.http import require_POST, require_GET
import reversion

from obcy.extras import prepare_view
from obcy.models import Joke
from obcy.management.commands.extras import clean_content
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


def unverified(request):
    context = prepare_view.unverified(request)
    return render(request, 'obce_all.html', context, context_instance=RequestContext(request))


@require_POST
def edit_joke(request, pk):
    body = request.POST.get('body', '')
    if not body:
        return HttpResponse(status=400)

    user = request.user.groups.filter(name='Moderator')
    if user:
        with transaction.atomic(), reversion.create_revision():
            joke = Joke.objects.get(pk=pk)
            joke.body = body
            joke.save()
            reversion.set_user(user)
            reversion.set_comment('Body updated.')
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


@require_GET
def clean_joke(request):
    body = request.GET.get('body', '')
    if not body:
        return HttpResponse(status=400)
    cleaned = clean_content(body)
    if cleaned != body:
        logger.debug('Cleaned body:\n%s\n------\n%s', body, cleaned)
    return JsonResponse({'cleaned': cleaned})


@require_POST
def verify_joke(request, pk):
    user = request.user.groups.filter(name='Moderator')
    if user:
        with transaction.atomic(), reversion.create_revision():
            joke = Joke.objects.get(pk=pk)
            joke.verified = timezone.localtime(timezone.now())
            joke.save()
            reversion.set_user(user)
            reversion.set_comment('Joke verified.')
            logger.info('Joke %s verified.', joke.key)
        return HttpResponse(status=200)
    else:
        return HttpResponse('User not authorised to verify joke')


@require_GET
def get_revisions(request, pk):
    user = request.user.groups.filter(name='Moderator')
    if user:
        joke = Joke.objects.get(pk=pk)
        version_list = reversion.get_unique_for_object(joke)
        versions = []
        for version in version_list:
            date = version.revision.date_created
            body = version.field_dict['body']
            versions.append({'date': date, 'body': body})
        return JsonResponse(versions, safe=False)
    else:
        return HttpResponse('User not authorised to get revisions')