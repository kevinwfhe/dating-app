from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid

from match.models import Match


# Assistance from https://stackoverflow.com/questions/2673647/enforce-unique-upload-file-names-using-django
def image_filename(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return filename

class Interest(models.Model):
    name = models.TextField(default="", blank=False, max_length=100)
class Profile(models.Model):
    GENDER = (
        ("MALE", "Male"),
        ("FEMALE", "Female"),
        ("OTHER", "Other"),
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
    about = models.TextField(max_length=500, default='', blank=True)
    interests = models.ManyToManyField(Interest)
    avatar = models.ImageField(upload_to=image_filename, blank=True)
    image = models.ImageField(upload_to=image_filename, blank=True)
    has_dated = models.BooleanField(default=False, blank=False)
    is_verified = models.CharField(choices=APPROVAL, default="TO BE APPROVED", blank=False, max_length=14)


    
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