from django.urls import path
from rest_framework.routers import DefaultRouter

from users.views import (
    JWTLoginView, 
    JWTLogoutView,
    JWTTokenRefreshView, 
    UserSignupViewSet,
    send_test_mail,
)


router = DefaultRouter()
router.register(r"signup", UserSignupViewSet, basename="user-signup")

urlpatterns = [
    path("token/login/", JWTLoginView.as_view(), name="obtain-token-login"),
    path("token/refresh/", JWTTokenRefreshView.as_view(), name="refresh-token"),
    path("token/logout/", JWTLogoutView.as_view(), name="blacklist-token-logout"),
    path("send-test-mail/", send_test_mail, name="send-test-mail"),
]

urlpatterns += router.urls
