import logging

from django.core.cache import cache
from django.db import transaction
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import django_filters
from rest_framework import viewsets, mixins
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
import reversion
from user_agents import parse

from obcy.models import Joke
from obcy.extras import prepare_view
from api.serializers import ObcyJokeSerializer
from api.models import Device
from api.commands import delete_joke as api_remove_joke

logger = logging.getLogger(__name__)


class ObcyJokeFilter(django_filters.FilterSet):
    before = django_filters.DateTimeFilter(name='added', lookup_type='lt')
    after = django_filters.DateTimeFilter(name='added', lookup_type='gt')
    min_votes = django_filters.NumberFilter(name='votes', lookup_type='gte')
    changed_after = django_filters.DateTimeFilter(name='changed', lookup_type='gt')

    class Meta:
        model = Joke
        fields = ['after', 'before', 'min_votes', 'changed_after']


class AllViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                 viewsets.GenericViewSet):
    serializer_class = ObcyJokeSerializer
    filter_class = ObcyJokeFilter
    lookup_field = 'key'
    paginate_by_param = 'limit'
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    queryset = Joke.objects.none()

    def get_queryset(self):
        jokes = Joke.objects.all().order_by('-added')
        if 'changed_after' not in self.request.GET:
            jokes = jokes.filter(hidden=None)

        return jokes

    def perform_destroy(self, instance):
        with transaction.atomic(), reversion.create_revision():
            instance.hidden = timezone.now()
            instance.save()
            logger.info('Joke %s removed via API.', instance.key)
            cache.clear()
            api_remove_joke(instance.key)


class RandomJokes(viewsets.ReadOnlyModelViewSet):
    serializer_class = ObcyJokeSerializer
    lookup_field = 'key'
    paginate_by_param = 'limit'

    def get_queryset(self):
        return prepare_view.random(self.request, pages=False)['jokes']


@csrf_exempt
@require_POST
def register_device(request):
    registration_id = request.POST.get('registration_id')
    android_id = request.POST.get('android_id')
    version = request.POST.get('version', '0.3.0')
    user_agent = parse(request.META['HTTP_USER_AGENT'])
    model = user_agent.device.family
    os_version = user_agent.os.version_string
    device_type = 'Mobile' if user_agent.is_mobile else 'Tablet'
    ip = get_client_ip(request)
    logger.debug(
        'register request from %s\nandroid_id = %s\napp_version = %s\nuser_agent = %s\nmodel = %s\nos_version = %s',
        ip, android_id, version, user_agent, model, os_version)
    try:
        device = Device.objects.get(android_id=android_id)
        device.registration_id = registration_id
        device.version = version
        device.model = model
        device.os_version = os_version
        device.type = device_type
        device.active = True
        device.last_seen = timezone.localtime(timezone.now())
        device.save()
        logger.debug('Device %s marked as last seen on %s', device.android_id, device.last_seen)
    except Device.DoesNotExist:
        Device.objects.create(registration_id=registration_id, android_id=android_id, version=version, model=model,
                              os_version=os_version, type=device_type)
        logger.info('Registered new device: %s', android_id)
    return HttpResponse(status=200)


@csrf_exempt
@require_POST
def deactivate_device(request):
    registration_id = request.POST.get('registration_id')
    try:
        device = Device.objects.get(registration_id=registration_id)
        device.active = False
        device.save()
    except Device.DoesNotExist:
        pass
    return HttpResponse(status=200)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
