from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Date, Winks, Reject, Match
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
import arrow
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from datetime import datetime as dt
# Create your views here.

@login_required
def match(request):
    current_user = request.user
    matches = Match.objects.filter(owner=request.user).order_by('-created_on')
    for match in matches:
      created_on = arrow.get(match.created_on)
      match.created_on = created_on.humanize()
    matches_paginated = Paginator(matches, 6)

    page = request.GET.get('page')
    try:
        matches_page = matches_paginated.page(page)
    except PageNotAnInteger:
        matches_page = matches_paginated.page(1)
        page = 1
    except EmptyPage:
        matches_page = matches_paginated.page(matches_paginated.num_pages)
        page = matches_paginated.num_pages
        
    
    context = {
        'page_ref': 'match',
        'matches_page': matches_page,
        'current_user': current_user,
        'page': page
    }
    
    
    return render(request, 'match.html', context)

@login_required
def winks(request):

    winks = Winks.objects.filter(receiver=request.user.id, is_wink_backed=False).order_by('-created_on')
    for wink in winks:
      created_on = arrow.get(wink.created_on)
      wink.created_on = created_on.humanize()
    winks_paginated = Paginator(winks, 6)

    page = request.GET.get('page')
    try:
        winks_page = winks_paginated.page(page)
    except PageNotAnInteger:
        winks_page = winks_paginated.page(1)
        page = 1
    except EmptyPage:
        winks_page = winks_paginated.page(winks_paginated.num_pages)
        page = winks_paginated.num_pages
        
    
    context = {
        'page_ref': 'wink',
        'winks_page': winks_page,
        'page': page
    }
    
    
    return render(request, 'winks.html', context)

def wink_back(request):
    receiver_id = request.GET.get('receiver_id')
    receiver = User.objects.get(pk=receiver_id)
    sender = request.user

    sender_match = Match(owner=sender, target=receiver)
    receiver_match = Match(owner=receiver, target=sender)
    sender_match.save()
    receiver_match.save()

    origin_wink = Winks.objects.get(sender=receiver, receiver=sender)
    origin_wink.is_wink_backed = True
    origin_wink.save()

    data = {}
    data['message'] = 'You two are matched!'
    return JsonResponse(data)

# AJAX function to create wink record 
def wink(request):
    
    # Get id of user recipient
    receiver_id = request.GET.get('receiver_id')
    # If user tried to wink at themselves
    if receiver_id == request.user.id:
        data = {}
        data['message'] = "You can't wink at yourself, cheeky!"
        return JsonResponse(data)


        
    # # Check if last wink send by request.user and received by recipient has been read
    current_wink = Winks.objects.filter(Q(receiver_id=receiver_id) & Q(sender_id=request.user.id)).exists()
    if current_wink:
        data = {}
        data['message'] = "Member hasn't viewed your last wink yet"
        return JsonResponse(data)

    # Create wink record
    receiver = User.objects.get(pk=receiver_id)
    wink = Winks(receiver=receiver, sender=request.user)

    data = {}
    try:
        wink.save()
    except:
        data['message'] = 'Something went wrong. Wink not sent'
    finally:
        data['message'] = 'Wink successfully sent.'
    return JsonResponse(data)

"""
AJAX function to create reject record. Used for quick match feature so as not to 
display a rejected user again
"""
def reject(request):
    # Get id of reject recipient
    receiver_id = request.GET.get('receiver_id')
    if receiver_id == request.user.id:
        return HttpResponse(status=204)
    
    # Check if a reject record for these users already exists, if so do nothing
    current_reject = Reject.objects.filter(Q(receiver_id=receiver_id) & Q(sender_id=request.user.id)).exists()
    if current_reject:
        return HttpResponse(status=204)
    
    # Create reject record
    reject = Reject(receiver=User.objects.get(pk=receiver_id), sender=request.user)
    data = {}
    try:
        reject.save()
    except:
        data['message'] = 'Something went wrong. Profile not skipped.'
    finally:
        data['message'] = 'Member successfully skipped'
    return JsonResponse(data)

class StartDate(APIView):
  authentication_classes = [authentication.SessionAuthentication]
  permission_classes = [permissions.IsAuthenticated]

  def post(self, request):
      initiator = request.user
      target_id = request.data['targetId'] 
      target = User.objects.get(pk=target_id)
      datetime = dt.fromtimestamp(request.data['datetime']/1000.0) 
      location = request.data['location']
      coupon_type = request.data['couponType']
      print(initiator, target, datetime, location, coupon_type)
      if target and initiator and datetime and location:
          date = Date(initiator=initiator, target=target, datetime=datetime, location=location, coupon_type=coupon_type)

          initiator_match = Match.objects.get(owner=initiator, target=target)
          target_match = Match.objects.get(owner=target, target=initiator)
          initiator_match.date = date
          initiator_match.date_scheduled = True
          target_match.date = date
          target_match.date_scheduled = True

          date.save()
          initiator_match.save()
          target_match.save()

          return HttpResponse(status=204)
      
      else:
        return JsonResponse({"message": "Please make sure your inputs are valid"})

class AcceptDate(APIView):
  authentication_classes = [authentication.SessionAuthentication]
  permission_classes = [permissions.IsAuthenticated]

  def post(self, request):
      target = request.user
      date_id = request.data['dateId'] 
      date = Date.objects.get(pk=date_id)
      if date.target == target:
          date.is_accepted = True
          date.save()
          return HttpResponse(status=204)
      
      else:
        return JsonResponse({"message": "You don't have access to do this."})