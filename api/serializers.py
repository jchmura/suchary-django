from django.utils import timezone
from rest_framework import serializers

from obcy.models import Joke


class DateTimeTzAwareField(serializers.DateTimeField):

    def to_native(self, value):
        if value:
            value = timezone.localtime(value)
            return super(DateTimeTzAwareField, self).to_native(value)


class ObcyJokeSerializer(serializers.ModelSerializer):
    added = DateTimeTzAwareField(source='added', format='%Y-%m-%dT%X%z')

    class Meta:
        model = Joke
        fields = ('key', 'votes', 'added', 'url', 'body', 'site')
