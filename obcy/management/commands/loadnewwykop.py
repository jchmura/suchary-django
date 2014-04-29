import json
import os
from time import sleep

from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
import pytz

from obcy.management.commands.extras import HTMLStripper, strip_tags, check_if_duplicate, inputJSON, notify_devices
from obcy.models import Joke


def create_model_object(joke):
    site = 'wykop'
    key = str(joke['id'])
    votes = joke['votes']
    date = joke['date']
    date = pytz.timezone("Europe/Warsaw").localize(date)
    url = joke['url']
    parser = HTMLStripper()
    parser.feed(joke['body'])
    body = strip_tags(parser.get_text())
    added = timezone.localtime(timezone.now())

    j = Joke(site=site, key=key, slug=key, votes=votes, date=date, url=url, body=body, added=added)
    j.save()

    return j


class Command(BaseCommand):
    help = 'Loads new jokes from wykop database'

    def __init__(self):
        super(Command, self).__init__()
        self.new_count = 0
        self.update_count = 0
        self.new_keys = []

    def handle(self, *args, **options):
        data = json.load(open(os.path.join(settings.BASE_DIR, 'data/wykop.json'), 'r'), object_hook=inputJSON)
        jokes = Joke.objects.filter(duplicate=None)

        for joke in data:
            if len(Joke.objects.filter(key=str(joke['id']))) == 0:
                sleep(2)
                new_joke = create_model_object(joke)
                if not check_if_duplicate(new_joke, jokes):
                    self.new_count += 1
                    self.new_keys.append(new_joke.key)
            else:
                old_joke = Joke.objects.get(key=str(joke['id']))
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
