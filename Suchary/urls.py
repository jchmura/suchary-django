from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView
from rest_framework import routers
from django.contrib import admin

from api.views import AllViewSet, RandomJokes


admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'obcy', AllViewSet, 'obcy')
router.register(r'random', RandomJokes, 'random')

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    # obcy
    url(r'^$', 'obcy.views.all_sites'),
    url(r'^obcy/random/$', 'obcy.views.all_random'),
    url(r'^obcy/unverified/$', 'obcy.views.unverified'),
    url(r'^obcy/(?P<jokeslug>.+)/$', 'obcy.views.one_joke'),
    url(r'^(wykop|codzienny|zacny)/(?P<key>.+)$',
        RedirectView.as_view(url='http://suchary.jakubchmura.pl/obcy/%(key)s', permanent=True)),
    url(r'^obcy/edit/(?P<pk>.+)$', 'obcy.views.edit_joke'),
    url(r'^obcy/delete/(?P<pk>.+)$', 'obcy.views.delete_joke'),
    url(r'^obcy/clean$', 'obcy.views.clean_joke'),
    url(r'^obcy/verify/(?P<pk>.+)$', 'obcy.views.verify_joke'),
    url(r'^obcy/revisions/(?P<pk>.+)$', 'obcy.views.get_revisions'),
    # autorski
    url(r'^autorskie/$', 'autorski.views.all_jokes'),
    url(r'^autorskie/(?P<jokeslug>.+)/$', 'autorski.views.one_joke'),
    # accounts
    url(r'^signin/', 'accounts.views.signin'),
    url(r'^signup/', 'accounts.views.signup'),
    url(r'^logout/', 'accounts.views.logout_view'),
    url(r'^fb-login/', 'accounts.views.fb_login'),
    # api
    url(r'^api/', include(router.urls)),
    url(r'^register/$', 'api.views.register_device'),
    url(r'^unregister/$', 'api.views.deactivate_device'),
    # other
    url(r'^favicon\.ico$', RedirectView.as_view(url='/media/images/favicon.ico')),
    url(r'^apk/$', RedirectView.as_view(url='/media/files/suchary.apk')),
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns += staticfiles_urlpatterns()