# Generated by Django 4.1.3 on 2022-11-14 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_interests_remove_profile_birth_date_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Interests',
            new_name='Interest',
        ),
    ]
