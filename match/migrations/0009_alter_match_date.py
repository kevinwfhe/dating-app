# Generated by Django 4.1.3 on 2022-11-23 01:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0008_alter_match_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='date',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='match.date'),
        ),
    ]
