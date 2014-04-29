import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
import pytz

from obcy.management.commands.extras import inputJSON, check_if_duplicate, remove_dots, notify_devices
from obcy.models import Joke


def _create_model_object(joke):
    site = 'sucharnia'
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
    help = 'Loads new jokes from sucharnia database'

    def __init__(self):
        super(Command, self).__init__()
        self.new_count = 0
        self.update_count = 0
        self.new_keys = []

    def handle(self, *args, **options):
        data = json.load(open(os.path.join(settings.BASE_DIR, 'data/sucharnia.json'), 'r'), object_hook=inputJSON)
        jokes = Joke.objects.filter(duplicate=None)

        for joke in data:
            if len(Joke.objects.filter(key=joke['id'])) == 0:
                new_joke = _create_model_object(joke)
                if not check_if_duplicate(new_joke, jokes):
                    self.new_count += 1
                    self.new_keys.append(new_joke.key)

            else:
                old_joke = Joke.objects.get(key=joke['id'])
                new_votes = joke['votes']
                if old_joke.votes < new_votes:
                    old_joke.votes = new_votes
                    old_joke.save()
                    self.update_count += 1

        if self.new_count:
            last = Joke.objects.latest('added')
            notify_devices(self.new_count, last.body, self.new_keys)

        self.stdout.write('Successfully added %d new jokes' % self.new_count)
        self.stdout.write('Successfully updated %d jokes' % self.update_count)
