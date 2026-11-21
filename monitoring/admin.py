from django.contrib import admin
from .models import NetworkDevice, MonitoringRecord


@admin.register(NetworkDevice)
class NetworkDeviceAdmin(admin.ModelAdmin):
    list_display = ("device_name", "ip_address", "device_type", "status", "last_checked")
    list_filter = ("status", "device_type")
    search_fields = ("device_name", "ip_address")


@admin.register(MonitoringRecord)
class MonitoringRecordAdmin(admin.ModelAdmin):
    list_display = ("device", "status", "response_time", "checked_at")
    list_filter = ("status",)
    readonly_fields = ("device", "status", "response_time", "checked_at")
