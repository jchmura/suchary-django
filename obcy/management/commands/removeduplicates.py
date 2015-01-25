from django.core.management.base import BaseCommand

from obcy.models import Joke


class Command(BaseCommand):
    def compare(self, set1, set2):
        len1 = len(set1)
        len2 = len(set2)

        if len1 < len2:
            count = self.count_number(set1, set2)
        else:
            count = self.count_number(set2, set1)

        if count / min(len1, len2) > 0.5:
            return True
        else:
            return False

    def count_number(self, set1, set2):
        count = 0
        for word in set1:
            if word in set2:
                count += 1
        return count

    def handle(self, *args, **options):

        dryrun = False
        if len(args) > 0 and args[0] == 'dryrun':
            print("Dry run")
            dryrun = True

        jokes = Joke.objects.filter(duplicate=None)

        for i, joke in enumerate(jokes[:]):
            set1 = set(joke.body.split())
            for secondJoke in jokes[i + 1:]:
                if joke.key != secondJoke.key:
                    set2 = set(secondJoke.body.split())
                    if self.compare(set1, set2):

                        if joke.votes > secondJoke.votes:
                            if not secondJoke.duplicate:
                                secondJoke.duplicate = joke
                                print(secondJoke.key, "(" + secondJoke.site + ")", "is duplicate of",
                                      joke.key, "(" + joke.site + ")")
                                if not dryrun:
                                    secondJoke.save()
                        else:
                            if not joke.duplicate:
                                joke.duplicate = secondJoke
                                print(joke.key, "(" + joke.site + ")", "is duplicate of", secondJoke.key,
                                      "(" + secondJoke.site + ")")
                                if not dryrun:
                                    joke.save()