# Generated by Django 4.1.3 on 2022-11-23 00:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('match', '0003_match'),
    ]

    operations = [
        migrations.CreateModel(
            name='Date',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_accepted', models.BooleanField(default=False)),
                ('datetime', models.DateTimeField()),
                ('location', models.CharField(default='', max_length=100)),
                ('is_first_date', models.BooleanField(default=False)),
                ('coupon_type', models.CharField(choices=[('RESERVATION', 'Free Reservation'), ('FLIGHT_COUPON', 'Flight Coupon')], default='RESERVATION', max_length=13)),
                ('initiator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='initiator', to=settings.AUTH_USER_MODEL)),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='date_target', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='match',
            name='date',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='match.date'),
        ),
    ]