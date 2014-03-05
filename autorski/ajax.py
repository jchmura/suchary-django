from django.conf.locale.pl.formats import DATETIME_FORMAT
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from django.utils.dateformat import DateFormat

from autorski.models import Joke


@dajaxice_register
def send_new(request, author, body):
    dajax = Dajax()

    joke = Joke(author=author, body=body)
    joke.save()

    body = body.replace('\n', '<br />')
    date = joke.date
    df = DateFormat(date)
    function = 'set_new("{}", "{}", "{}", "{}");'.format(author, df.format(DATETIME_FORMAT), joke.pk, body)
    dajax.script(function)

    return dajax.json()