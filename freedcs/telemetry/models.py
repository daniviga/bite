from django.db import models
from django.contrib.postgres.fields import JSONField

from api.models import Device


class Telemetry(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    time = models.DateTimeField(primary_key=True, auto_now_add=True)
    payload = JSONField()

    class Meta:
        ordering = ['time', 'device']
        verbose_name_plural = "Telemetry"

    def __str__(self):
        return "%s - %s" % (self.time, self.device.serial)
