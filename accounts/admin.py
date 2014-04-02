from django.contrib import admin

from accounts.models import FacebookUser


class FacebookUserAdmin(admin.ModelAdmin):
    list_display = ['uid', 'username', 'user']


admin.site.register(FacebookUser, FacebookUserAdmin)