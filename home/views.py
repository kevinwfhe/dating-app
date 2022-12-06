from django.shortcuts import render
from profiles.models import Profile, ProfileImage
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import datetime as DT

# Home page after user logs in
@login_required
def index(request):

    # Profiles for quick match finder, exclude users winked or rejected previously
    if request.user.profile.looking_for == "BOTH":
        card_profiles = Profile.objects.filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).filter(user__is_staff=False).exclude(user_id=request.user.id).all()[:10]
    else:
        card_profiles = Profile.objects.filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).filter(user__is_staff=False).filter(gender=request.user.profile.looking_for).exclude(user_id=request.user.id).all()[:10]

    current_user_interests = request.user.profile.interests.all()
    matched_profile = []
    for profile in card_profiles:
      match = False
      for interest in profile.interests.all():
        if interest in current_user_interests:
          match = True
      if match:
        matched_profile.append(profile)

    if matched_profile.__len__ == 0:
        card_profiles_exists = False
    else: 
        card_profiles_exists = True

    context = {
        'page_ref': 'home',
        'card_profiles_exists' : card_profiles_exists,
        'card_profiles': matched_profile,
        'has_filled_profile': request.user.profile.has_filled_profile,
    }
    
    return render(request, 'home.html', context)
    
# Home page before logged in/registered
def preregister(request):
        
    return render(request, 'index.html')