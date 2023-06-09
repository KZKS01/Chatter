# Generated by Django 4.2.1 on 2023-06-11 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0028_like_like_icon_url'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='like',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='post',
            name='like_icon_url',
            field=models.CharField(default='https://k-chatter.s3.us-east-2.amazonaws.com/App+pics/like+icon.svg', max_length=200),
        ),
        migrations.RemoveField(
            model_name='like',
            name='like_icon_url',
        ),
    ]
