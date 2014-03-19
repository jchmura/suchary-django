from django.core.management.base import BaseCommand

from obcy.models import Joke


class Command(BaseCommand):
    def handle(self, *args, **options):
        jokes = Joke.objects.filter(site='wykop')
        for joke in jokes:
            lines = joke.body.split('\n')
            for word in lines[-1].split():
                if word[0] != '#':
                    break
            else:
                del lines[-1]

            for word in lines[0].split():
                if word[0] != '#':
                    break
            else:
                del lines[0]

            for i, line in reversed(list(enumerate(lines))):
                if line == '':
                    del lines[i]

            body = '\n'.join(lines)
            joke.body = body
            joke.save()