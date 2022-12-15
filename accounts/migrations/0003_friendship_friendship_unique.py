# Generated by Django 4.1.1 on 2022-12-12 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_friendship_follow"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="friendship",
            constraint=models.UniqueConstraint(
                fields=("followee", "follower"), name="friendship_unique"
            ),
        ),
    ]