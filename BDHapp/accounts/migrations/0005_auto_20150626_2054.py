# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20150626_2045'),
    ]

    operations = [
        migrations.CreateModel(
            name='perm_request',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('new_permission', models.CharField(default=b'CE', max_length=2, choices=[(b'CE', b'COPY ED'), (b'SW', b'SENIOR STAFF WRITER'), (b'SE', b'SECTION ED'), (b'EB', b'EDIT BOARD')])),
                ('req', models.CharField(default=b'CU', max_length=2, choices=[(b'CU', b'CREATE USER'), (b'CP', b'CHANGE PERMISSION')])),
                ('by', models.ForeignKey(to='accounts.BDHuser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='request',
            name='by',
        ),
        migrations.DeleteModel(
            name='request',
        ),
    ]
