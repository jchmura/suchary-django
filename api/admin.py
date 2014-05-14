from django.contrib import admin

from api.models import Device


class DeviceAdmin(admin.ModelAdmin):
    list_display = ['android_id', 'created', 'last_used', 'active']
    list_filter = ['active']
    search_fields = ['registration_id', 'android_id']


admin.site.register(Device, DeviceAdmin)
