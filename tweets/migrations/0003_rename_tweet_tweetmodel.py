# Generated by Django 4.1.1 on 2022-11-19 02:38

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("tweets", "0002_tweet_author_tweet_created_date_tweet_text"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Tweet",
            new_name="TweetModel",
        ),
    ]