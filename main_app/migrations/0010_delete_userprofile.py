# Generated by Django 4.2 on 2023-04-27 03:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_alter_userprofile_avatar'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]