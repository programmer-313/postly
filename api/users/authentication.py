from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


class FixedJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user = super().get_user(validated_token)
        token_version = validated_token["token_version"]

        if str(user.token_version) != token_version:
            raise AuthenticationFailed("You are already logged out.")
        
        if not user.is_verified:
            raise AuthenticationFailed("User is unverified. verify your account before loggin in.")

        return user
