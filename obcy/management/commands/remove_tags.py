from django.core.management.base import BaseCommand
from obcy.management.commands.extras import remove_dots

from obcy.models import Joke


class Command(BaseCommand):
    def handle(self, *args, **options):
        jokes = Joke.objects.all()
        for joke in jokes:
            lines = joke.body.split('\n')

            for word in lines[-1].split():
                if word[0] != '#':
                    break
            else:
                del lines[-1]

            if not lines:
                continue

            for word in lines[0].split():
                if word[0] != '#':
                    break
            else:
                del lines[0]

            found = False
            for i, line in reversed(list(enumerate(lines))):
                if line == '':
                    if not found:
                        found = True
                    else:
                        del lines[i]

            body = '\n'.join(lines)
            joke.body = remove_dots(body)
            joke.save()