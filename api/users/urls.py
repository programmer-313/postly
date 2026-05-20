from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)


urlpatterns = [
    path("token/login/", TokenObtainPairView.as_view(), name="obtain_token_login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh_token"),
    path("token/blacklist/", TokenBlacklistView.as_view(), name="blacklist_token")
]