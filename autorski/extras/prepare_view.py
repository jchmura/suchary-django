from functools import reduce
import operator

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

from autorski.models import Joke


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
    user = request.user
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


def all_jokes(request, pages=True):
    sort = request.GET.get('sort', 'date')

    reverse = request.GET.get('reversed', True)
    if reverse != 'true':
        reverse = True
    else:
        reverse = False

    context = {}
    jokes = Joke.objects.all()
    search = request.GET.get('q', '')
    if search.strip() != '':
        items = search.split()
        filter = reduce(operator.and_, (Q(body__icontains=x) for x in items))
        jokes = jokes.filter(filter)
        context.update({'search': search})

    jokes = sorted(jokes, key=lambda joke: joke.__getattribute__(sort), reverse=reverse)
    if pages:
        jokes = __add_pages(request, jokes)
    context.update({'jokes': jokes})
    __add_user(request, context)

    return context


def one_joke(request, id):
    joke = Joke.objects.get(pk=id)
    context = {'joke': joke}
    __add_user(request, context)
    return context