# Generated by Django 4.2 on 2023-04-25 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default='default_avatar', upload_to='avatars'),
        ),
    ]
