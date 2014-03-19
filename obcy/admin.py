from django.contrib import admin

from obcy.models import Joke


class JokeAdmin(admin.ModelAdmin):
    list_display = ['site', 'key', 'votes', 'date', 'added', 'duplicate']
    list_filter = ['date']
    search_fields = ['body', 'key']


admin.site.register(Joke, JokeAdmin)
