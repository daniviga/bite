import uuid

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


def device_validation(value):
    if settings.SKIP_WHITELIST and settings.DEBUG:
        return  # skip validation in debug mode when SKIP_WHITELIST is True

    published_devices = WhiteList.objects.filter(
        serial=value,
        is_published=True
    )
    if not published_devices:
        raise ValidationError("Device is not published")


class WhiteList(models.Model):
    serial = models.CharField(max_length=128, unique=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['serial', 'updated_time']

    def __str__(self):
        return self.serial


class Device(models.Model):
    serial = models.CharField(max_length=128, unique=True,
                              validators=[device_validation])
    uuid = models.UUIDField(unique=True, default=uuid.uuid4,
                            editable=False)
    creation_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['updated_time', 'serial']

    def __str__(self):
        return self.serial
