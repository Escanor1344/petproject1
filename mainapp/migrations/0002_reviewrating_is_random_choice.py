# Generated by Django 4.1.1 on 2022-10-14 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewrating',
            name='is_random_choice',
            field=models.BooleanField(default=False),
        ),
    ]
