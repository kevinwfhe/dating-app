# Generated by Django 4.1.3 on 2022-11-15 23:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_profile_avatar_alter_profile_gender'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='bio',
            new_name='about',
        ),
    ]
