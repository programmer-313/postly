from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import JWTLoginView, JWTLogoutView, send_test_mail



urlpatterns = [
    path("token/login/", JWTLoginView.as_view(), name="obtain_token_login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh_token"),
    path("token/blacklist/", JWTLogoutView.as_view(), name="blacklist_token"),
    path("send-test-mail/", send_test_mail, name="send-test-mail"),
]
