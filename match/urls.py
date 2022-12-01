from django.urls import path
from .views import winks, match

urlpatterns = [
    path('', match, name='match'),
    path('winks/', winks, name="winks"),
]