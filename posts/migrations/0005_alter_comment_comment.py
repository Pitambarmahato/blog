# Generated by Django 3.2.3 on 2021-06-03 14:16

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_alter_comment_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.TextField(default=datetime.datetime(2021, 6, 3, 14, 16, 18, 827417, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
