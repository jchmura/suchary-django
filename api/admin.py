from django.contrib import admin

from api.models import Device


class DeviceAdmin(admin.ModelAdmin):
    list_display = ['created', 'last_used', 'active']
    list_filter = ['active']
    search_fields = ['registration_id']


admin.site.register(Device, DeviceAdmin)
