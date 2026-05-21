from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class FixedTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # add the customized token version (uuid value) from user table
        token["token_version"] = str(user.token_version)

        return token