from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax

from autorski.models import Joke


@dajaxice_register
def send_new(request, author, body):
    dajax = Dajax()

    joke = Joke(author=author, body=body)
    joke.save()

    date = joke.date.strftime("%e %B %Y %X")
    function = 'set_new("{}", "{}", "{}", "{}");'.format(author, date, joke.pk, body)
    dajax.script(function)

    return dajax.json()