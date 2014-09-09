from django.contrib import admin

from api.models import Device


class DeviceAdmin(admin.ModelAdmin):
    list_display = ['android_id', 'alias', 'model', 'os_version', 'version', 'created', 'last_seen', 'active']
    list_filter = ['active']
    search_fields = ['registration_id', 'android_id', 'alias']


admin.site.register(Device, DeviceAdmin)
