from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Winks, Reject
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
# Create your views here.

@login_required
def winks(request):

    winks = Winks.objects.filter(receiver=request.user.id).order_by('-created_on')
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


# AJAX function to create wink record 
def wink(request):
    
    # Get id of user recipient
    receiver_id = request.GET.get('receiver_id')
    # If user tried to wink at themselves
    if receiver_id == request.user.id:
        data = {}
        data['message'] = "You can't wink at yourself, cheeky!"
        return JsonResponse(data)
        
    # Check if last wink send by request.user and received by recipient has been read
    current_wink = Winks.objects.filter(Q(receiver_id=receiver_id) & Q(sender_id=request.user.id) & Q(is_read=False)).exists()
    if current_wink:
        data = {}
        data['message'] = "Member hasn't viewed your last wink yet"
        return JsonResponse(data)
    
    # Create wink record
    wink = Winks(receiver=User.objects.get(pk=receiver_id), sender=request.user)
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