from django.contrib import admin

from autorski.models import Joke


class JokeAdmin(admin.ModelAdmin):
    list_display = ['author', 'votes', 'date']
    list_filter = ['date']
    search_fields = ['body', 'author']

admin.site.register(Joke, JokeAdmin)
