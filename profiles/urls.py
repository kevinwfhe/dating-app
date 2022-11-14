from profiles.views import logout, login, register, member_profile, delete, verification_message
from profiles import url_reset
from django.urls import path, include
        
urlpatterns = [
    path('logout/', logout, name='logout'),
    path('login/', login, name='login'), 
    path('register/', register, name='register'),
    path('delete/', delete, name="delete"),
    path('verification-message/', verification_message, name="verification_message"),
    path('member/(?P<id>\d+)', member_profile, name='member_profile'),
    path('password-reset/', include(url_reset))
]