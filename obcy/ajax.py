import logging

from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax

from api.commands import edit_joke as api_edit_joke
from api.commands import delete_joke as api_remove_joke
from obcy.models import Joke


logger = logging.getLogger(__name__)


@dajaxice_register
def delete_joke(request, pk):
    dajax = Dajax()

    user = request.user.groups.filter(name='Moderator')
    if user:
        joke = Joke.objects.get(pk=pk)
        joke.hidden = True
        joke.save()
        function = 'deleted_joke({})'.format(pk)
        logger.info('Joke %s removed.', joke.key)
        api_remove_joke(joke.key)
    else:
        function = 'alert("User not authorised to remove joke");'

    dajax.script(function)

    return dajax.json()


@dajaxice_register
def edit_joke(request, pk, body):
    dajax = Dajax()

    user = request.user.groups.filter(name='Moderator')
    if user:
        joke = Joke.objects.get(pk=pk)
        joke.body = body
        joke.save()
        function = 'edited_joke({})'.format(pk)
        logger.info('Joke %s edited.', joke.key)
        api_edit_joke(joke.key)
    else:
        function = 'alert("User not authorised to edit joke");'

    dajax.script(function)

    return dajax.json()