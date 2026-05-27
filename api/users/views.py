from django.http import JsonResponse
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import (
    TokenObtainPairView, 
    TokenBlacklistView,
    TokenRefreshView,
)


import uuid

from users.serializers import FixedTokenObtainPairSerializer, FixedTokenRefreshSerializer
from users.models import User


# add the fixed serializer classes for the login and refresh view in order to add token version in returned data
class JWTLoginView(TokenObtainPairView):
    serializer_class = FixedTokenObtainPairSerializer


class JWTTokenRefreshView(TokenRefreshView):
    serializer_class = FixedTokenRefreshSerializer


class JWTLogoutView(TokenBlacklistView):

    def post(self, request, *args, **kwargs):
        # obtain user id from refresh token
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            user_id = token["user_id"]
            response = super().post(request, *args, **kwargs)

            if response.status_code == 200:
                user = User.objects.get(id=user_id)
                # update the token version from user table
                user.token_version = uuid.uuid4()
                user.save()

            return response
        except TokenError as e:
            error = {
                "detail": str(e),
                "code": "token_not_valid"
            }
            return Response(error, status=status.HTTP_401_UNAUTHORIZED)


def send_test_mail(request):
    send_mail(
        "Testing Email",
        "Checking if email services are working."
        "API Test mail",
        "admin@example.com",
        ["user1@example.com"],
        fail_silently=False,
    )
    return JsonResponse({"status": "test mail sent successfully."})
