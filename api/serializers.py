from rest_framework import serializers

from obcy.models import Joke


class ObcyJokeSerializer(serializers.ModelSerializer):
    added = serializers.DateTimeField(source='added', format='%Y-%m-%dT%XZ')

    class Meta:
        model = Joke
        fields = ('key', 'votes', 'date', 'added', 'url', 'body', 'site')
