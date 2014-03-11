from functools import reduce
import operator

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

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


def all_sites(request, pages=True):
    sort = request.GET.get('sort', 'date')

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

    return context


def one_joke(jokeslug):
    joke = Joke.objects.get(slug=jokeslug)
    site_url = SITE_URL[joke.site]
    site_image_extension = SITE_IMAGE_EXTENSION[joke.site]
    context = {'joke': joke, 'site_url': site_url, 'site_image_extension': site_image_extension}
    return context