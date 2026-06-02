from django.urls import path
from rest_framework.routers import DefaultRouter

from users.views import (
    JWTLoginView, 
    JWTLogoutView,
    JWTTokenRefreshView, 
    UserSignupViewSet,
    UserSendOTPViewSet,
)


router = DefaultRouter()
router.register(r"signup", UserSignupViewSet, basename="user-signup")
router.register(r"send_otp", UserSendOTPViewSet, basename="user-send-otp")

urlpatterns = [
    path("token/login/", JWTLoginView.as_view(), name="obtain-token-login"),
    path("token/refresh/", JWTTokenRefreshView.as_view(), name="refresh-token"),
    path("token/logout/", JWTLogoutView.as_view(), name="blacklist-token-logout"),
]

urlpatterns += router.urls
