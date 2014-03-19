from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax

from obcy.models import Joke


@dajaxice_register
def delete_joke(request, pk):
    dajax = Dajax()

    user = request.user.groups.filter(name='Moderator')
    if user:
        joke = Joke.objects.get(pk=pk)
        joke.delete()
        function = 'deleted_joke({})'.format(pk)
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
    else:
        function = 'alert("User not authorised to edit joke");'

    dajax.script(function)

    return dajax.json()