# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20150623_1904'),
    ]

    operations = [
        migrations.CreateModel(
            name='requests',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('req', models.CharField(default=b'CU', max_length=2, choices=[(b'CU', b'CREATE USER'), (b'CP', b'CHANGE PERMISSION')])),
                ('approved_rejected_by', models.ForeignKey(to='accounts.author')),
                ('by', models.ForeignKey(to='accounts.BDHuser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
