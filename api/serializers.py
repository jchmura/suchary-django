from rest_framework import serializers

from obcy.models import Joke


class ObcyJokeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Joke
        fields = ('key', 'votes', 'date', 'added', 'url', 'body')
