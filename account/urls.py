from django.urls import path, re_path
from .views import management, public_profile, personal_information, cancel_subscription, reactivate_subscription

urlpatterns = [
    path('profile/', public_profile, name='public_profile'),
    path('personal/', personal_information, name='personal_information'),
    path('management/', management, name='management'),
    re_path(r'^cancel/(?P<subscription_id>[0-9A-Za-z_]+)$', cancel_subscription, name='cancel_subscription'),
    re_path(r'^reactivate/(?P<subscription_id>[0-9A-Za-z_]+)$', reactivate_subscription, name='reactivate_subscription')]