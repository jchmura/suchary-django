import logging

from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import django_filters
from rest_framework import viewsets
from user_agents import parse

from obcy.models import Joke
from obcy.extras import prepare_view
from api.serializers import ObcyJokeSerializer
from api.models import Device


logger = logging.getLogger(__name__)


class ObcyJokeFilter(django_filters.FilterSet):
    before = django_filters.DateTimeFilter(name='added', lookup_type='lt')
    after = django_filters.DateTimeFilter(name='added', lookup_type='gt')
    min_votes = django_filters.NumberFilter(lookup_type='gte')

    class Meta:
        model = Joke
        fields = ['after', 'before', 'min_votes']


class AllViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ObcyJokeSerializer
    filter_class = ObcyJokeFilter
    lookup_field = 'key'
    paginate_by_param = 'limit'

    def get_queryset(self):
        return prepare_view.all_sites(self.request, pages=False)['jokes']

    def get_object(self, queryset=None):
        return prepare_view.one_joke(self.request, self.kwargs['key'])['joke']


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
    logger.info(
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