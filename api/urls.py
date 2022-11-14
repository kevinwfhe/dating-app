from django.urls import include, path
from account.views import DeleteAccount
from profiles.views import InitialProfile

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('delete_account/', DeleteAccount.as_view()),
    path('initial_profile/', InitialProfile.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]