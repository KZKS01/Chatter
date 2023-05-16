# Generated by Django 4.2 on 2023-05-16 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0011_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='avatar_url',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.CharField(default='https://s3.us-east-2.amazonaws.com/k-chatter/713d6b.PNG', max_length=200),
        ),
    ]
