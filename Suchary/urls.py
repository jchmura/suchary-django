from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView
from rest_framework import routers
from django.contrib import admin
from Suchary import settings

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
    # obcy
    url(r'^$', 'obcy.views.all_sites'),
    url(r'^obcy/random/$', 'obcy.views.all_random'),
    url(r'^obcy/(?P<jokeslug>.+)/$', 'obcy.views.one_joke'),
    url(r'^(wykop|codzienny|zacny)/(?P<key>.+)$',
        RedirectView.as_view(url='http://suchary.jakubchmura.pl/obcy/%(key)s', permanent=True)),
    # autorski
    url(r'^autorskie/$', 'autorski.views.all_jokes'),
    url(r'^autorskie/(?P<jokeslug>.+)/$', 'autorski.views.one_joke'),
    # accounts
    url(r'^signin/', 'accounts.views.signin'),
    url(r'^signup/', 'accounts.views.signup'),
    url(r'^logout/', 'accounts.views.logout_view'),
    url(r'^fb-login/', 'accounts.views.fb_login'),
    # api
    url(r'^api', include(router.urls)),
    # other
    url(r'^favicon\.ico$', RedirectView.as_view(url='/media/images/favicon.ico')),
    url(r'^apk/$', RedirectView.as_view(url='/media/files/suchary.apk')),
    url(r'^test/$', 'autorski.views.test'),

)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()