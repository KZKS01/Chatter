# Generated by Django 4.2 on 2023-04-24 02:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_rename_post_photo_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photo', to='main_app.post'),
        ),
    ]
