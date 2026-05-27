from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import (
    JWTLoginView, 
    JWTLogoutView,
    JWTTokenRefreshView, 
    send_test_mail,
)



urlpatterns = [
    path("token/login/", JWTLoginView.as_view(), name="obtain_token_login"),
    path("token/refresh/", JWTTokenRefreshView.as_view(), name="refresh_token"),
    path("token/logout/", JWTLogoutView.as_view(), name="blacklist_token_logout"),
    path("send-test-mail/", send_test_mail, name="send-test-mail"),
]
