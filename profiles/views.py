from django.shortcuts import render, redirect, reverse
from django.contrib import auth
from django.forms import modelformset_factory
from profiles.forms import UserLoginForm, UserRegistrationForm, ProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from .models import Profile, ProfileImage
from rest_framework.views import APIView
from rest_framework import authentication, permissions
import base64
from django.core.files.base import ContentFile
    
"""
Function to check if member profiles matches with current user's sexuality (and 
vice versa). This stops users from visiting profiles outside of their preferences
"""
def looking_for_check(request, user_one, user_two):
    if not user_one == user_two:
        if user_one.looking_for == "MALE":
            if not user_two.gender == "MALE":
                return redirect(reverse('index'))
        elif user_one.looking_for == "FEMALE":
            if not user_two.gender == "FEMALE":
                return redirect(reverse('index'))

# Return users height in feet and inches from form choices
def height_choices(member_height):
    height = {
        "152.40": "5' 0",
        "154.94":"5' 1",
        "157.48":"5' 2",
        "160.02":"5' 3",
        "162.56":"5' 4",
        "165.10":"5' 5",
        "167.64":"5' 6",
        "170.18":"5' 7",
        "172.72":"5' 8",
        "175.26":"5' 9",
        "177.80":"5' 10",
        "180.34":"5' 11",
        "182.88":"6' 0",
        "185.42":"6' 1",
        "187.96":"6' 2",
        "190.50":"6' 3",
        "193.04":"6' 4",
        "195.58":"6' 5",
        "198.12":"6' 6",
        "200.66":"6' 7",
        "203.20":"6' 8",
        "205.74":"6' 9",
        "208.28":"6' 10",
        "210.82":"6' 11"
        }
        
    return height[member_height]

# URL to log user out
@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, "You have been logged out")
    return redirect(reverse('preregister'))

# URL to delete user
@login_required
def delete(request):
    try:
        user = User.objects.get(pk=request.user.id)
        user.delete()
        messages.success(request, "Your account has been deleted") 
    except:
        messages.success(request, "Something went wrong. Please contact us for more information") 
        
    return redirect(reverse('preregister'))

# Log in page
def login(request):
    # If user is already logged in
    if request.user.is_authenticated:
        return redirect(reverse('index'))
        
    # If user submits log in form, try logging them in
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
            if user:
                messages.success(request, "Logged in successfully")
                auth.login(user=user, request=request)
                return redirect(reverse('index'))
            else: 
                messages.error(request, "Username or password incorrect")
    else:
        login_form = UserLoginForm()
            
    context = {
        'login_form':login_form
    }
    return render(request, 'login.html', context)
    
# Register a user account page
def register(request):
    # If user submits register form, try registering an account
    if request.method == "POST":
        registration_form = UserRegistrationForm(request.POST)

        if registration_form.is_valid():
            registration_form.save()
            
            user = auth.authenticate(username=request.POST['username'], password=request.POST['password1'])
            
            if user:
                messages.success(request, "Your account had been created")
                auth.login(user=user, request=request)
                return redirect(reverse('index'))
            else:
                messages.error(request, "We have been unable to create your account")
    else:
        registration_form = UserRegistrationForm()
        

    context = {
        'registration_form':registration_form
    }
    return render(request, 'register.html', context)  

# Page to view a specific member profile
@login_required 
def member_profile(request, id):
    
    # Check is member if current user
    member = User.objects.get(id=id)
    if not member == request.user:
        current_user = False
        
        # Redirect if sexuality preferences are not met
        result = looking_for_check(request, request.user.profile, member.profile)
        if result:
            return result
        result = looking_for_check(request, member.profile, request.user.profile)
        if result:
            return result
        
        # Add view if last view is not read or user hasn't viewed member before
        # last_view = Views.objects.filter(receiver_id=id).filter(sender_id=request.user.id).last()
        # if not last_view or last_view.is_read:
        #     view = Views(receiver=member, sender=request.user)
        #     view.save()
        
        # If user has submitted messages form
        # if request.method == "POST" and 'message_submit' in request.POST:
        #     message_form = MessagesForm(request.POST)
        #     if message_form.is_valid():
        #         # Check if user is premium
        #         if request.user.profile.is_premium:
        #             customer_stripe_id = Subscription.objects.filter(user_id=request.user).first()
        #             customer = stripe.Customer.retrieve(customer_stripe_id.customer_id)
        #             for sub in customer.subscriptions:
        #                 # If subscription is active or unpaid/cancelled but not yet inactive
        #                 if sub.status == 'active' or sub.status == 'trialing' or sub.status == 'incomplete' or sub.status == 'past_due' or sub.status == 'canceled':
        #                     # Create conversation (if one does not already exist) and message
        #                     conversation = Conversations.objects.filter(participants=request.user.id).filter(participants=id)
        #                     if conversation.exists():
        #                         message = message_form.save(commit=False)
        #                         message.sender = request.user
        #                         message.receiver = User.objects.get(pk=id)
        #                         message.conversation = conversation[0]
        #                         message.save()
        #                         return redirect('/chat/%s' % conversation[0].id )
        #                     else:
        #                         receiver = User.objects.get(pk=id)
        #                         conversation = Conversations()
        #                         conversation.save()
        #                         conversation.participants.add(request.user.id)
        #                         conversation.participants.add(receiver)
        #                         message = message_form.save(commit=False)
        #                         message.sender = request.user
        #                         message.receiver = receiver
        #                         message.conversation = conversation
        #                         message.save()
        #                         return redirect('/chat/%s' % conversation.id )
                                
        #             """
        #             If user is premium, but does not have an active subscription
        #             update them to not be premium
        #             """
        #             current_user = User.objects.get(pk=request.user.id)
        #             current_user.is_premium = False
        #             current_user.save()
        #             return redirect(reverse('subscribe'))
        #         else:
        #             return redirect(reverse('subscribe'))
        # else:
        #     message_form = MessagesForm()
    else:
        # message_form = MessagesForm()
        current_user = True
        
    context = {
        'page_ref' : 'member_profile',
        'member' : member,
        'current_user' : current_user
    }
    return render(request, 'member.html', context)
    
# Page to display verification message
def verification_message(request):
    
    return render(request, 'verification-message.html')

class InitialProfile(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        profile = Profile.objects.get(user=request.user)
        profile.age = request.data["age"]
        profile.location = request.data["loc"]
        profile.gender = request.data["gender"]
        profile.relationship_status = request.data["relationship_status"]
        for i in request.data["interests"]:
          profile.interests.add(i)
        # finish profile filling for the first time 
        profile.has_filled_profile = True
        profile.save()
        return HttpResponse(status=204)

class UploadAvatar(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        profile = Profile.objects.get(user=request.user)
        avatar_str = request.data['avatar']
        format, imgstr = avatar_str.split(';base64,') 
        ext = format.split('/')[-1] 
        avatar = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        profile.avatar = avatar
        profile.save()
        return HttpResponse(status=204)

class UploadImage(APIView):
  authentication_classes = [authentication.SessionAuthentication]
  permission_classes = [permissions.IsAuthenticated]

  def post(self, request):
      profile = Profile.objects.get(user=request.user)
      image_str = request.data['image']
      format, imgstr = image_str.split(';base64,') 
      ext = format.split('/')[-1] 
      image = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
      profile.image = image
      profile.save()
      return HttpResponse(status=204)