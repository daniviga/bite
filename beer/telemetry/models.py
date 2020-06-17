from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.postgres.fields import JSONField

from api.models import Device


class Telemetry(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    time = models.DateTimeField(primary_key=True, auto_now_add=True)
    transport = models.CharField(max_length=4,
                                 choices=[('http', 'http'), ('mqtt', 'mqtt')],
                                 default='http')
    clock = models.IntegerField(
        validators=[MinValueValidator(0)],
        null=True)
    payload = JSONField()

    class Meta:
        ordering = ['-time', 'device']
        verbose_name_plural = "Telemetry"

    def __str__(self):
        return str(self.time)
