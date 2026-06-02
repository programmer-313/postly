from typing import Any
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer
)


# get the user model for using it in serializers
User = get_user_model()


# serializers for jwt token authentication
class FixedTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    modify validate method to add the token version to returned token pair
    """
    def validate(self, attrs: dict[str, Any]) -> dict[str, str]:
        data =  super().validate(attrs)

        # obtain user, and add its token_version to the returned data
        user = self.user
        data["token_version"] = str(user.token_version)
        
        return data 


class FixedTokenRefreshSerializer(TokenRefreshSerializer):
    """
    modify the validate method to add the token version to be returned data along with access token
    """
    def validate(self, attrs: dict[str, Any]) -> dict[str, str]:
        data = super().validate(attrs)

        # obtain user_id from refresh token and get token version for that user
        refresh_token = self.token_class(attrs["refresh"])
        user_id = refresh_token["user_id"]

        User = get_user_model()
        user = User.objects.get(pk=user_id)
        data["token_version"] = str(user.token_version)

        return data

    # depricated code
    # @classmethod
    # def get_token(cls, user):
    #     token = super().get_token(user)

    #     # add the customized token version (uuid value) from user table
    #     token["token_version"] = str(user.token_version)

    #     return token


# serializers for user sign up and adding otp feature
class UserSignupSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = User
            fields = ["email", "password"]


class UserSendOTPSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["otp_version"]


class UserVerifyOTPSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["otp_version", "otp_code"]
