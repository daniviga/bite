# Generated by Django 3.1.3 on 2021-03-19 08:08

import api.models
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('serial', models.CharField(max_length=128, unique=True, validators=[api.models.device_validation])),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['updated_time', 'serial'],
            },
        ),
        migrations.CreateModel(
            name='WhiteList',
            fields=[
                ('serial', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('is_published', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['serial', 'updated_time'],
            },
        ),
    ]
