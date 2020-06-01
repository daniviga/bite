from django.contrib import admin
from telemetry.models import Telemetry


@admin.register(Telemetry)
class TelemetryAdmin(admin.ModelAdmin):
    readonly_fields = ('device', 'time', 'payload',)
