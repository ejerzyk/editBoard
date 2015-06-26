# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author_url', models.CharField(max_length=20)),
                ('section', models.CharField(default=b'N', max_length=2, choices=[(b'M', b'METRO'), (b'N', b'UNIVERSITY NEWS'), (b'AC', b'ARTS & CULTURE'), (b'SR', b'SCIENCE & RESEARCH'), (b'S', b'SPORTS')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BDHuser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('class_year', models.IntegerField()),
                ('phone_number', models.CharField(max_length=10)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='author',
            name='gen_user',
            field=models.ForeignKey(to='accounts.BDHuser', unique=True),
            preserve_default=True,
        ),
    ]
