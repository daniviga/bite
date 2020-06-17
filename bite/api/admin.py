from django.contrib import admin
from api.models import Device, WhiteList


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    readonly_fields = ('creation_time', 'updated_time',)
    list_filter = ('serial',)
    search_fields = ('serial',)

    fieldsets = (
        (None, {
            'fields': ('serial', )
        }),
        ('Audit', {
            'classes': ('collapse',),
            'fields': ('creation_time', 'updated_time',)
        }),
    )


@admin.register(WhiteList)
class WhiteListAdmin(admin.ModelAdmin):
    readonly_fields = ('creation_time', 'updated_time',)
    list_filter = ('serial',)
    search_fields = ('serial',)

    fieldsets = (
        (None, {
            'fields': ('serial', 'is_published',)
        }),
        ('Audit', {
            'classes': ('collapse',),
            'fields': ('creation_time', 'updated_time',)
        }),
    )
