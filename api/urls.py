from django.urls import include, path
from account.views import DeleteAccount
from profiles.views import InitialProfile, UploadAvatar, UploadImage, UpdateInterests
from match.views import wink, reject, wink_back, StartDate, AcceptDate

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('delete_account/', DeleteAccount.as_view()),
    path('initial_profile/', InitialProfile.as_view()),
    path('upload_avatar/', UploadAvatar.as_view()),
    path('upload_image/', UploadImage.as_view()),
    path('update_interests/', UpdateInterests.as_view(), name="update_interests"),
    path('wink/', wink, name="wink"),
    path('wink_back/', wink_back, name="wink_back"),
    path('reject/', reject, name="reject"),
    path('start_date/', StartDate.as_view(), name="start_date"),
    path('accept_date/', AcceptDate.as_view(), name="accept_date"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]