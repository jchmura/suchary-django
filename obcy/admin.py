from django.contrib import admin
import reversion

from obcy.models import Joke


class JokeAdmin(reversion.VersionAdmin):
    list_display = ['site', 'key', 'votes', 'added', 'duplicate', 'hidden']
    list_filter = ['added', 'hidden']
    search_fields = ['body', 'key']


admin.site.register(Joke, JokeAdmin)
