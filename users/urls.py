from rest_framework.routers import DefaultRouter
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from .views import UserAPISet, UserAPIModelSet

router = DefaultRouter()
# router.register('', UserAPISet, basename='users-list')
router.register('', UserAPIModelSet, basename='users-list')

# urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('login', obtain_auth_token, name='login')
]

# urlpatterns = [
#     path('', UserAPISet.as_view({'get':'list'}))
# ]