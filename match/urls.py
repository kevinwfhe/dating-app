from django.urls import path
from .views import winks

urlpatterns = [
    path('winks/', winks, name="winks"),
]