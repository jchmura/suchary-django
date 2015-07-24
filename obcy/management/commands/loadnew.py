import json
import logging
import os
from time import sleep

from django.core.cache import cache
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
import pytz
import reversion

from api.commands import new_jokes
from obcy.management.commands.extras import input_json, is_duplicate, HTMLStripper, clean_content
from obcy.models import Joke

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def __init__(self):
        super(Command, self).__init__()
        self.new_count = 0
        self.update_count = 0
        self.site = None

    def create_joke(self, joke):
        key = joke['id']
        votes = joke['votes']
        date = joke['date']
        date = pytz.timezone("Europe/Warsaw").localize(date)
        added = timezone.localtime(timezone.now())

        if self.site == 'wykop':
            url = joke['url']
            parser = HTMLStripper()
            parser.feed(joke['body'])
            body = parser.get_text()
        else:
            url = 'http://facebook.com/' + key.replace("_", "/posts/")
            body = joke['body']

        body = clean_content(body)

        return Joke(site=self.site, key=key, slug=key, url=url, votes=votes, date=date, body=body, added=added)

    def handle(self, *args, **options):
        if len(args) != 1:
            return

        self.site = args[0]

        data = json.load(open(os.path.join(settings.BASE_DIR, 'data/{}.json'.format(self.site)), 'r'),
                         object_hook=input_json)
        jokes = Joke.objects.filter(duplicate=None)

        for joke in data:
            if len(Joke.objects.filter(key=joke['id'])) == 0:
                sleep(2)
                new_joke = self.create_joke(joke)
                logger.info('Created new joke: %s from site %s', new_joke.key, new_joke.site)
                if not is_duplicate(new_joke, jokes):
                    self.new_count += 1
                with transaction.atomic(), reversion.create_revision():
                    new_joke.save()
                    reversion.set_comment('Joke creation.')
            else:
                old_joke = Joke.objects.get(key=joke['id'])
                new_votes = joke['votes']
                if old_joke.votes < new_votes:
                    old_joke.votes = new_votes
                    old_joke.save()
                    self.update_count += 1

        if self.new_count:
            cache.clear()
            new_jokes()

        self.stdout.write('Successfully added %d new jokes' % self.new_count)
        self.stdout.write('Successfully updated %d jokes' % self.update_count)
