# Generated by Django 2.0 on 2018-01-01 17:09

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('egamen', '0020_auto_20180101_1640'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserProfile',
            new_name='UserProfiles',
        ),
    ]