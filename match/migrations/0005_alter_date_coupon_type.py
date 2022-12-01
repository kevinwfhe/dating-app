# Generated by Django 4.1.3 on 2022-11-23 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0004_date_match_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='date',
            name='coupon_type',
            field=models.CharField(choices=[('RESERVATION', 'Free Reservation'), ('FLIGHT_COUPON', 'Flight Coupon')], default=None, max_length=13, null=True),
        ),
    ]
