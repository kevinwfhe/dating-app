from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Winks(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winks_sender", unique=False)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winks_receiver", unique=False)
    created_on = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False, blank=False)
    is_wink_backed = models.BooleanField(default=False, blank=False)

class Reject(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rejected_sender", unique=False)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rejected_receiver", unique=False)
    created_on = models.DateTimeField(auto_now_add=True)

class Date(models.Model):
    COUPON_TYPE = (
        ('RESERVATION', 'Free Reservation'),
        ('FLIGHT_COUPON', 'Flight Coupon'),
    )
    initiator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='initiator')
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name='date_target')
    is_accepted = models.BooleanField(default=False, blank=False)
    datetime = models.DateTimeField()
    location = models.CharField(max_length=100, default='', blank=False)
    is_first_date = models.BooleanField(default=False, blank=False)
    coupon_type = models.CharField(choices=COUPON_TYPE, default=None, max_length=13, blank=False, null=True)

class Match(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name='target')
    created_on = models.DateTimeField(auto_now_add=True)
    date = models.ForeignKey(Date, on_delete=models.CASCADE, default=None, null=True, blank=True)