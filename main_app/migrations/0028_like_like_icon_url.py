# Generated by Django 4.2.1 on 2023-06-11 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0027_remove_post_like_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='like_icon_url',
            field=models.CharField(default='https://k-chatter.s3.us-east-2.amazonaws.com/App+pics/like+icon.svg', max_length=200),
        ),
    ]
