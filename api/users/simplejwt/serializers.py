from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication


class RefreshJWTSerializer(TokenRefreshSerializer):
    def validate(self, attrs: dict[str, any]) -> dict[str, any]:
        data = super().validate(attrs)

        jwt_authentication = JWTAuthentication()

        validated_token = jwt_authentication.get_validated_token(data["access"])
        user = jwt_authentication.get_user(validated_token)

        data["first_name"] = str(user.first_name)
        data["last_name"] = str(user.last_name)
        data["picture_url"] = str(user.picture_url)
        data["email"] = str(user.email)

        return data
