from django.http import JsonResponse
from django.utils import timezone
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
    UserSignupSerializer,
    UserSendOTPSerializer,
    UserVerifyOTPSerializer,
)
from users.utils import (
    generate_otp_code,
    send_email_user_otp,
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
class UserSignupViewSet(
    viewsets.GenericViewSet, 
    mixins.CreateModelMixin
    ):
    queryset = None
    serializer_class = UserSignupSerializer

    def create(self, request, *args, **kwargs):
        user_serializer = self.get_serializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)

        # get the user data from serializer and create inactive user
        user_data = user_serializer.validated_data
        user = User(email=user_data.get("email"))
        user.set_password(user_data.get("password"))
        user.otp_created_at = timezone.now() - timezone.timedelta(seconds=120)
        user.save()

        return Response(
            status=status.HTTP_201_CREATED, 
            data={
                "detail": "Inactive user created successfully.",
                "user_id": str(user.id),
                "otp_version": str(user.otp_version),
            }
        )


# now create the viewset to send/resend otp to the user
class UserSendOTPViewSet(
    viewsets.GenericViewSet,
    mixins.UpdateModelMixin
    ):
    queryset = User.objects.all()
    serializer_class = UserSendOTPSerializer
    http_method_names = ["patch", "options", "head"]    # we are omitting "put" provided by this mixin

    def partial_update(self, request, *args, **kwargs):
        user = self.get_object()
        user_serializer = self.get_serializer(user, data=request.data, partial=True)
        user_serializer.is_valid(raise_exception=True)

        user_data = user_serializer.validated_data    # it returns the data types same as serializer fields 
        request_user_otp_version = user_data.get("otp_version")

        if user.is_active or user.is_verified:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "detail": "User is already verified.",
                    "code": "user_already_verified"
                }
            )
        else:
            if not (
                str(user.otp_version) == str(request_user_otp_version)
            ):
                return Response(
                    data={
                        "detail": "Invalid Request",
                        "code": "bad_request",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                if user.otp_created_at + timezone.timedelta(seconds=120) <= timezone.now():
                    user.otp_code = generate_otp_code()
                    user.otp_version = uuid.uuid4()
                    user.otp_created_at = timezone.now()
                    user.save()
                    
                    send_email_user_otp(
                        user_otp_code=str(user.otp_code),
                        user_email=user.email,
                    )

                    return Response(
                        data={
                            "detail": "Enter OTP sent to your Email for Account Verification.",
                            "code": "otp_sent_to_email",
                            "user_id": str(user.id),
                            "otp_version": str(user.otp_version),
                        },
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        data={
                            "detail": "You can request for resending otp after 2 minutes",
                            "code": "request_too_early"
                        },
                        status=status.HTTP_425_TOO_EARLY
                    )


# create viewset to verify user otp and make the user verified
class UserVerifyOTPViewSet():
    ...



