# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-27 21:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('author', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=50)),
                ('imageUrl', models.CharField(default='images/default.jpg', max_length=256)),
                ('participation', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
