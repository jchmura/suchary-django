from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView
from rest_framework import routers
from django.contrib import admin

from api.views import AllViewSet

admin.autodiscover()

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

router = routers.DefaultRouter()
router.register(r'/obcy', AllViewSet, 'obcy')

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'^$', 'obcy.views.all_sites'),
    url(r'^obcy/(?P<jokeslug>.+)/$', 'obcy.views.one_joke'),
    url(r'^api', include(router.urls)),
    url(r'^autorskie/$', 'autorski.views.all_jokes'),
    url(r'^test/$', 'obcy.views.test'),
    url(r'^(wykop|codzienny|zacny)/(?P<key>.+)$',
        RedirectView.as_view(url='http://suchary.jakubchmura.pl/obcy/%(key)s', permanent=True)),
    url(r'^favicon.ico$', RedirectView.as_view(url='/media/images/favicon.ico')),
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()