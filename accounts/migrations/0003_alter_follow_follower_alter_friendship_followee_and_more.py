# Generated by Django 4.1.1 on 2022-12-10 14:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_follow_friendship_follow_follower_follow_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="follow",
            name="follower",
            field=models.ManyToManyField(
                through="accounts.Friendship", to="accounts.follow"
            ),
        ),
        migrations.AlterField(
            model_name="friendship",
            name="followee",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="friendship_followee",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="friendship",
            name="follower",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="friendship_follower",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]