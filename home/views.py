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
        card_profiles = Profile.objects.filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).exclude(user_id=request.user.id).all()[:10]
    else:
        card_profiles = Profile.objects.filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).filter(gender=request.user.profile.looking_for).exclude(user_id=request.user.id).all()[:10]
    
    if card_profiles.count() == 0:
        card_profiles_exists = False
    else: 
        card_profiles_exists = True
    
    
    today = DT.date.today()
    one_week_ago = today - DT.timedelta(days=7)
    # Profiles for active most recently, excluding those who signed up in the last 7 days
    if request.user.profile.looking_for == "BOTH":
        active_profiles = Profile.objects.filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).filter(user__date_joined__lte=one_week_ago).order_by('-user__last_login').exclude(user_id=request.user.id).all()[:4]
    else:
        active_profiles = Profile.objects.filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).filter(gender=request.user.profile.looking_for).filter(user__date_joined__lte=one_week_ago).order_by('-user__last_login').exclude(user_id=request.user.id).all()[:4] 
    
    # Profiles ordered by signed up date for 'Newcomers' section
    if request.user.profile.looking_for == "BOTH":
        newest_profiles = Profile.objects.filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).order_by('-user__date_joined').exclude(user_id=request.user.id).all()[:4]
    else:
        newest_profiles = Profile.objects.filter(Q(looking_for=request.user.profile.gender) | Q(looking_for="BOTH")).filter(gender=request.user.profile.looking_for).order_by('-user__date_joined').exclude(user_id=request.user.id).all()[:4] 

    context = {
        'page_ref': 'home',
        'card_profiles_exists' : card_profiles_exists,
        'active_profiles':active_profiles,
        'newest_profiles': newest_profiles,
        'card_profiles': card_profiles,
        'has_filled_profile': request.user.profile.has_filled_profile,
    }
    
    return render(request, 'home.html', context)
    
# Home page before logged in/registered
def preregister(request):
        
    return render(request, 'index.html')