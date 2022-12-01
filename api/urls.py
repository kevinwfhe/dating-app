from django.urls import include, path
from account.views import DeleteAccount
from profiles.views import InitialProfile, UploadAvatar, UploadImage
from match.views import wink, reject, wink_back, StartDate

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('delete_account/', DeleteAccount.as_view()),
    path('initial_profile/', InitialProfile.as_view()),
    path('upload_avatar/', UploadAvatar.as_view()),
    path('upload_image/', UploadImage.as_view()),
    path('wink/', wink, name="wink"),
    path('wink_back/', wink_back, name="wink_back"),
    path('reject/', reject, name="reject"),
    path('start_date/', StartDate.as_view(), name="start_date"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]