# Generated by Django 5.0.4 on 2024-04-11 09:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_apikey'),
    ]

    operations = [
        migrations.DeleteModel(
            name='apiKey',
        ),
        migrations.DeleteModel(
            name='News',
        ),
    ]
