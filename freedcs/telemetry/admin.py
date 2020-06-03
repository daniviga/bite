from django.contrib import admin
from telemetry.models import Telemetry


@admin.register(Telemetry)
class TelemetryAdmin(admin.ModelAdmin):
    readonly_fields = ('device', 'time', 'clock', 'payload',)
    list_display = ('__str__', 'device')
    list_filter = ('time', 'device__serial')
    search_fields = ('device__serial',)
