import json
import os
from time import sleep

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
import pytz
from api.commands import new_jokes

from obcy.management.commands.extras import inputJSON, check_if_duplicate, remove_dots
from obcy.models import Joke


def _create_model_object(joke):
    site = 'zacny'
    key = joke['id']
    slug = key
    url = 'http://facebook.com/' + key.replace("_", "/posts/")
    votes = joke['votes']
    date = joke['date']
    date = pytz.timezone("Europe/Warsaw").localize(date)
    body = remove_dots(joke['body'])
    added = timezone.localtime(timezone.now())

    j = Joke(site=site, key=key, slug=slug, url=url, votes=votes, date=date, body=body, added=added)
    j.save()

    return j


class Command(BaseCommand):
    help = 'Loads new jokes from suchar codzienny\'s database'

    def __init__(self):
        super(Command, self).__init__()
        self.new_count = 0
        self.update_count = 0

    def handle(self, *args, **options):
        data = json.load(open(os.path.join(settings.BASE_DIR, 'data/zacny.json'), 'r'), object_hook=inputJSON)
        jokes = Joke.objects.filter(duplicate=None)

        for joke in data:
            if len(Joke.objects.filter(key=joke['id'])) == 0:
                sleep(2)
                new_joke = _create_model_object(joke)
                if not check_if_duplicate(new_joke, jokes):
                    self.new_count += 1

            else:
                old_joke = Joke.objects.get(key=joke['id'])
                new_votes = joke['votes']
                if old_joke.votes < new_votes:
                    old_joke.votes = new_votes
                    old_joke.save()
                    self.update_count += 1

        if self.new_count:
            new_jokes()

        self.stdout.write('Successfully added %d new jokes' % self.new_count)
        self.stdout.write('Successfully updated %d jokes' % self.update_count)
