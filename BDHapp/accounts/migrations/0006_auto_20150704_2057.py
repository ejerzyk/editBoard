# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20150626_2054'),
    ]

    operations = [
        migrations.CreateModel(
            name='author_relationship',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('author', models.ForeignKey(to='accounts.author')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='editor_relationship',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('editor', models.ForeignKey(to='accounts.author')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='story',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('section', models.CharField(max_length=2, choices=[(b'M', b'METRO'), (b'N', b'UNIVERSITY NEWS'), (b'AC', b'ARTS & CULTURE'), (b'SR', b'SCIENCE & RESEARCH'), (b'S', b'SPORTS')])),
                ('url', models.CharField(max_length=150)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='editor_relationship',
            name='story',
            field=models.ForeignKey(to='accounts.story'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='author_relationship',
            name='story',
            field=models.ForeignKey(to='accounts.story'),
            preserve_default=True,
        ),
    ]
