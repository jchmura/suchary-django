from rest_framework import viewsets

from obcy.extras import prepare_view
from api.serializers import ObcyJokeSerializer


class AllViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ObcyJokeSerializer
    lookup_field = 'key'
    paginate_by_param = 'limit'

    def get_queryset(self):
        return prepare_view.all_sites(self.request, pages=False)['jokes']