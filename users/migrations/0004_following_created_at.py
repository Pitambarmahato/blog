# Generated by Django 3.2.3 on 2021-06-08 14:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_following'),
    ]

    operations = [
        migrations.AddField(
            model_name='following',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2021, 6, 8, 14, 44, 23, 815404, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
