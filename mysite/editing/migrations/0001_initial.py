# Generated by Django 3.1.7 on 2021-03-27 16:55

from django.db import migrations, models
import gallery.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Overlay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='static/overlays', validators=[gallery.validators.validate_size])),
            ],
        ),
    ]
