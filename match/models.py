from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Winks(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winks_sender", unique=False)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winks_receiver", unique=False)
    created_on = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False, blank=False)

class Reject(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rejected_sender", unique=False)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rejected_receiver", unique=False)
    created_on = models.DateTimeField(auto_now_add=True)