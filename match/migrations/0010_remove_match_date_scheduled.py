# Generated by Django 4.1.3 on 2022-11-23 01:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0009_alter_match_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='date_scheduled',
        ),
    ]
