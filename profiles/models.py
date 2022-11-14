from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid
import datetime
import os
import math
from django.db.models.expressions import RawSQL
from django.http import HttpResponse
import stripe
from django.db.backends.signals import connection_created
from django.dispatch import receiver
import os


class Interest(models.Model):
    name = models.TextField(default="", blank=False, max_length=100)
class Profile(models.Model):
    GENDER = (
        ("MALE", "Male"),
        ("FEMALE", "Female")
    )
    LOOKING_FOR = (
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('BOTH', 'Both'),
    )
    RELATIONSHIP_STATUS = (
        ('SINGLE', 'Single'),
        ('IN_RELATIONSHIP', 'In relationship'),
    )
    APPROVAL = (
        ('TO BE APPROVED', 'To be approved'),
        ('APPROVED', 'Approved'),
        ('NOT APPROVED', 'Not approved')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    has_filled_profile = models.BooleanField(default=False)
    age = models.IntegerField(blank=False, default=0)
    gender = models.CharField(choices=GENDER, default="MALE", max_length=6, blank=False)
    relationship_status = models.CharField(choices=RELATIONSHIP_STATUS, default="SINGLE", blank=False, max_length=100)
    location = models.CharField(max_length=100, default='', blank=False)
    looking_for = models.CharField(choices=LOOKING_FOR, default='BOTH', blank=False, max_length=6)
    bio = models.TextField(max_length=500, default='', blank=True)
    interests = models.ManyToManyField(Interest)

    # Additional info that might be used in the futuer
    # hair_length = models.CharField(choices=HAIR_LENGTH, default="LONG", blank=False, max_length=100)
    # ethnicity = models.CharField(choices=ETHNICITY, default="WHITE", blank=False, max_length=100)
    # education = models.CharField(choices=EDUCATION, default="HIGH SCHOOL", blank=False, max_length=100)
    # height = models.DecimalField(max_digits=10, default=180.34, decimal_places=2)
    # hair_colour = models.CharField(choices=HAIR_COLOUR, default="BLACK", blank=False, max_length=10)
    # body_type = models.CharField(choices=BODY_TYPE, default="AVERAGE", blank=False, max_length=15)
    # children = models.BooleanField(default=False)
    # citylat = models.DecimalField(max_digits=9, decimal_places=6, default='-2.0180319')
    # citylong = models.DecimalField(max_digits=9, decimal_places=6, default='52.5525525')
    # birth_date = models.DateField(null=True, default='1990-01-01', blank=True)
    # is_premium = models.BooleanField(default=False)
    is_verified = models.CharField(choices=APPROVAL, default="TO BE APPROVED", blank=False, max_length=14)
    
    # objects = LocationManager()

# Assistance from https://stackoverflow.com/questions/2673647/enforce-unique-upload-file-names-using-django
def image_filename(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('images/', filename)
    
class ProfileImage(models.Model):
    
    APPROVAL = (
        ('TO BE APPROVED', 'To be approved'),
        ('APPROVED', 'Approved'),
        ('NOT APPROVED', 'Not approved')
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    image = models.ImageField(upload_to=image_filename, blank=True)
    is_verified = models.CharField(choices=APPROVAL, default="TO BE APPROVED", blank=False, max_length=14)



    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
    
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)

def pre_delete_user(sender, instance, **kwargs):
    print(sender, instance)
    # Before user deleted
    pass
        
pre_delete.connect(pre_delete_user, sender=User)