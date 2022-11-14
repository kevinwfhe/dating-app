from django.urls import path
from .views import index, preregister

urlpatterns = [
    path('', preregister, name='preregister'),
    path('home/', index, name="index"),
]
