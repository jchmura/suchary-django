import logging

from django.core.cache import cache
from django.db import transaction
from django.utils import timezone

from rest_framework import serializers
import reversion

from obcy.models import Joke
from api.commands import edit_joke as api_edit_joke

logger = logging.getLogger(__name__)


class DateTimeTzAwareField(serializers.DateTimeField):

    def to_native(self, value):
        if value:
            value = timezone.localtime(value)
            return super(DateTimeTzAwareField, self).to_native(value)


class ObcyJokeSerializer(serializers.ModelSerializer):
    added = DateTimeTzAwareField(format='%Y-%m-%dT%X%z')
    changed = DateTimeTzAwareField(format='%Y-%m-%dT%X%z')
    hidden = DateTimeTzAwareField(format='%Y-%m-%dT%X%z')

    def update(self, instance, validated_data):
        instance.body = validated_data.get('body', instance.body)
        with transaction.atomic(), reversion.create_revision():
            instance.save()
            reversion.set_comment('Body updated via API.')
            logger.info('Joke %s edited.', instance.key)
            cache.clear()
            api_edit_joke(instance.key)
        return instance

    class Meta:
        model = Joke
        fields = ('key', 'votes', 'added', 'url', 'body', 'site', 'changed', 'hidden')
