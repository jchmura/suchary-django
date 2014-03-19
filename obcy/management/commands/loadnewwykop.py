from datetime import datetime
from html.parser import HTMLParser
import json
import os

from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
import pytz

from obcy.models import Joke


def inputJSON(obj):
    newDic = {}

    for key in obj:
        try:
            if float(key) == int(float(key)):
                newKey = int(key)
            else:
                newKey = float(key)

            newDic[newKey] = obj[key]
            continue
        except ValueError:
            pass

        try:
            newDic[str(key)] = datetime.strptime(obj[key], '%Y-%m-%d %H:%M:%S')
            continue
        except (TypeError, ValueError):
            pass

        newDic[str(key)] = obj[key]

    return newDic


class HTMLStripper(HTMLParser):
    def __init__(self):
        super(HTMLStripper, self).__init__()
        self.text = ""

    def handle_data(self, data):
        self.text += data

    def get_text(self):
        return self.text


def compare(set1, set2):
    len1 = len(set1)
    len2 = len(set2)

    if len1 < len2:
        count = count_number(set1, set2)
    else:
        count = count_number(set2, set1)

    if count / min(len1, len2) > 0.8:
        return True
    else:
        return False


def count_number(set1, set2):
    count = 0
    for word in set1:
        if word in set2:
            count += 1
    return count


def check_if_duplicate(joke, jokes):
    set1 = set(joke.body.split())

    for second_joke in jokes:
        if second_joke == joke:
            continue
        set2 = set(second_joke.body.split())
        if compare(set1, set2):
            if joke.votes > second_joke.votes:
                if not second_joke.duplicate:
                    second_joke.duplicate = joke
                    second_joke.save()
            else:
                if not joke.duplicate:
                    joke.duplicate = second_joke
                    joke.save()
            return True
    else:
        return False


def strip_tags(body):
    lines = body.split('\n')
    for word in lines[-1].split():
        if word[0] != '#':
            break
    else:
        del lines[-1]

    for i, line in reversed(list(enumerate(lines))):
        if line == '':
            del lines[i]

    body = '\n'.join(lines)
    return body


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

    def handle(self, *args, **options):
        data = json.load(open(os.path.join(settings.BASE_DIR, 'data/wykop.json'), 'r'), object_hook=inputJSON)
        jokes = Joke.objects.filter(duplicate=None)

        for joke in data:
            if len(Joke.objects.filter(key=str(joke['id']))) == 0:
                new_joke = create_model_object(joke)
                if not check_if_duplicate(new_joke, jokes):
                    self.new_count += 1
            else:
                old_joke = Joke.objects.get(key=str(joke['id']))
                new_votes = joke['votes']
                if old_joke.votes < new_votes:
                    old_joke.votes = new_votes
                    old_joke.save()
                    self.update_count += 1

        self.stdout.write('Successfully added %d new jokes' % self.new_count)
        self.stdout.write('Successfully updated %d jokes' % self.update_count)
