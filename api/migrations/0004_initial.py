# Generated by Django 5.0.4 on 2024-04-11 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api', '0003_delete_apikey_delete_news'),
    ]

    operations = [
        migrations.CreateModel(
            name='apiKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_key', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('updated', models.DateTimeField(auto_now=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
