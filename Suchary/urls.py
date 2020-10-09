from django.conf.urls import include, url
from django.views.generic.base import RedirectView
from rest_framework import routers
from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token

from api.views import AllViewSet, RandomJokes
import obcy.views as obcy
import api.views as api
import accounts.views as accounts

admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'obcy', AllViewSet, 'obcy')
router.register(r'random', RandomJokes, 'random')

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    # obcy
    url(r'^$', obcy.all_sites),
    url(r'^obcy/random/$', obcy.all_random),
    url(r'^obcy/unverified/$', obcy.unverified),
    url(r'^obcy/(?P<jokeslug>.+)/$', obcy.one_joke),
    url(r'^(wykop|codzienny|zacny)/(?P<key>.+)$',
        RedirectView.as_view(url='/obcy/%(key)s', permanent=True)),
    url(r'^obcy/edit/(?P<pk>.+)$', obcy.edit_joke),
    url(r'^obcy/delete/(?P<pk>.+)$', obcy.delete_joke),
    url(r'^obcy/duplicate/(?P<pk>.+)/(?P<key>.+)$', obcy.duplicate_joke),
    url(r'^obcy/clean$', obcy.clean_joke),
    url(r'^obcy/verify/(?P<pk>.+)$', obcy.verify_joke),
    url(r'^obcy/revisions/(?P<pk>.+)$', obcy.get_revisions),
    # autorski
    # url(r'^autorskie/$', 'autorski.views.all_jokes'),
    # url(r'^autorskie/(?P<jokeslug>.+)/$', 'autorski.views.one_joke'),
    # accounts
    url(r'^signin/', accounts.signin),
    url(r'^signup/', accounts.signup),
    url(r'^logout/', accounts.logout_view),
    url(r'^fb-login/', accounts.fb_login),
    # api
    url(r'^api/', include(router.urls)),
    url(r'^register/$', api.register_device),
    url(r'^unregister/$', api.deactivate_device),
    url(r'^api/token/$', obtain_auth_token),
    # other
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico', permanent=True)),
    url(r'^apk/$', RedirectView.as_view(url='/static/files/suchary.apk', permanent=True)),
]

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns += staticfiles_urlpatterns()
