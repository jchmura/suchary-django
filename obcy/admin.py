from django.contrib import admin
import reversion

from obcy.models import Joke


class JokeAdmin(reversion.VersionAdmin):
    list_display = ['site', 'key', 'votes', 'date', 'added', 'duplicate', 'hidden']
    list_filter = ['date', 'hidden']
    search_fields = ['body', 'key']


admin.site.register(Joke, JokeAdmin)
