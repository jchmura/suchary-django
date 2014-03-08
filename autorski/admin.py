from django.contrib import admin

from autorski.models import Joke, User


class JokeAdmin(admin.ModelAdmin):
    list_display = ['author', 'effective_votes', 'date']
    list_filter = ['date']
    search_fields = ['body', 'author']

    def effective_votes(self, obj):
        return obj.votes

admin.site.register(Joke, JokeAdmin)
