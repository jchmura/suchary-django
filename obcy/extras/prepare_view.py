from functools import reduce
import operator
import datetime

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.utils.timezone import make_aware, get_current_timezone
import time

from obcy.models import Joke


SITE_URL = {
    'wykop': 'http://wykop.pl',
    'codzienny': 'https://facebook.com/sucharcodzienny',
    'zacny': 'https://www.facebook.com/1zacnysucharmilordzie1',
    'sucharnia': 'https://www.facebook.com/groups/495903230481274'
}
SITE_IMAGE_EXTENSION = {
    'wykop': 'png',
    'codzienny': 'jpg',
    'zacny': 'jpg',
    'sucharnia': 'png'
}


def __sort_recalculate(sort, joke):
    if sort == 'votes':
        votes = joke.votes
        if joke.site == 'wykop' or joke.site == 'sucharnia':
            votes *= 4.5
        return votes
    else:
        return joke.__getattribute__(sort)


def __add_pages(request, jokes):
    paginator = Paginator(jokes, 15)
    page = request.GET.get('page')
    try:
        jokes = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        jokes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        jokes = paginator.page(paginator.num_pages)
    return jokes


def __add_user(request, context):
    page = request.GET.get('page', 1)
    user = request.user
    if page != 1:
        if user.is_authenticated():
            if user.first_name:
                name = user.first_name
                if user.last_name:
                    name += ' ' + user.last_name
            else:
                name = user.username
            username = user.username
        else:
            name = None
            username = None

        context.update({'user_fullname': name, 'username': username})

    moderator = True if user.groups.filter(name='Moderator') else False
    context.update({'moderator': moderator})


def __last_seen(request):
    last = request.session.get('last_seen', False)
    request.session['last_seen'] = time.time()
    return last


def all_sites(request, pages=True):
    sort = request.GET.get('sort', 'added')
    if sort == 'date':
        sort = 'added'

    reverse = request.GET.get('reversed', True)
    if reverse != 'true':
        reverse = True
    else:
        reverse = False

    context = {}
    jokes = Joke.objects.filter(duplicate=None)
    search = request.GET.get('q', '')
    if search.strip() != '':
        items = search.split()
        filter = reduce(operator.and_, (Q(body__icontains=x) for x in items))
        jokes = jokes.filter(filter)
        context.update({'search': search})

    jokes = sorted(jokes, key=lambda joke: __sort_recalculate(sort, joke), reverse=reverse)
    if pages:
        jokes = __add_pages(request, jokes)
    context.update({'jokes': jokes, 'site': 'all'})

    context.update({'site_image_extension': SITE_IMAGE_EXTENSION})

    __add_user(request, context)

    last_seen = __last_seen(request)
    if last_seen and time.time()-last_seen > 1:
        context.update({'last_seen': make_aware(datetime.datetime.fromtimestamp(last_seen+1), get_current_timezone())})

    return context


def one_joke(request, jokeslug):
    joke = Joke.objects.get(slug=jokeslug)
    site_url = SITE_URL[joke.site]
    site_image_extension = SITE_IMAGE_EXTENSION[joke.site]
    context = {'joke': joke, 'site_url': site_url, 'site_image_extension': site_image_extension}
    __add_user(request, context)
    return context


def random(request):
    jokes = Joke.objects.filter(duplicate=None).order_by('?')
    jokes = __add_pages(request, jokes)
    context = {'jokes': jokes, 'site': 'all', 'site_image_extension': SITE_IMAGE_EXTENSION, 'random': True}
    __add_user(request, context)
    return context