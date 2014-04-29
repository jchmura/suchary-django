from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import django_filters
from rest_framework import viewsets

from obcy.models import Joke
from obcy.extras import prepare_view
from api.serializers import ObcyJokeSerializer
from api.models import Device


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
    try:
        device = Device.objects.get(registration_id=registration_id)
        device.active = True
        device.save()
    except Device.DoesNotExist:
        Device.objects.create(registration_id=registration_id)
    return HttpResponse(status=201)


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