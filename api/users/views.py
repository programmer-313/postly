from django.http import JsonResponse
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import (
    TokenObtainPairView, 
    TokenBlacklistView,
    TokenRefreshView,
)
import uuid

from users.serializers import (
    FixedTokenObtainPairSerializer, 
    FixedTokenRefreshSerializer,
    UserSignupSerializer
)


# get the user model for views
User = get_user_model()


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
        

# views for user sign up and otp verification
class UserSignupViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # get the user data from serializer and create inactive user
        user_data = serializer.validated_data
        user = User(email=user_data.get("email"))
        user.set_password(user_data.get("password"))
        user.otp_created_at = timezone.now() - timezone.timedelta(seconds=120, microseconds=0.1)
        user.save()

        return Response(status=status.HTTP_201_CREATED, data={"detail": "Inactive user created successfully."})



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
