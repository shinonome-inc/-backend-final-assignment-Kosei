# Generated by Django 4.1.1 on 2022-11-28 02:18

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tweets", "0003_rename_tweet_tweetmodel"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tweetmodel",
            name="created_date",
        ),
        migrations.AddField(
            model_name="tweetmodel",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
