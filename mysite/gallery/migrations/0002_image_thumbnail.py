# Generated by Django 3.1.7 on 2021-03-27 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='static/thumbnails'),
        ),
    ]