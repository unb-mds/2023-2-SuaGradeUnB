from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework.test import APITestCase
from users.models import User
from rest_framework import status
from django.urls import reverse
from http.cookies import SimpleCookie
from django.http import HttpResponse


class UserSessionLogoutTests(APITestCase):

    def setUp(self):
        self.user, _ = User.objects.get_or_create(
            first_name="test",
            last_name="banana",
            picture_url="https://photo.aqui.com",
            email="uiui@pichuruco.com")
        self.user.save()

        self.refresh_token = TokenObtainPairSerializer.get_token(self.user)

    def make_logout_post_request(self, cookie_enable: bool = True, cookie_value: str | None = None) -> HttpResponse:
        if cookie_enable:
            self.client.cookies = SimpleCookie(
                {'refresh': self.refresh_token if not cookie_value else cookie_value}
            )

        url = reverse('users:logout')
        return self.client.post(url, {}, format='json')

    def test_logout_user_with_valid_token(self):
        response = self.make_logout_post_request()

        jti_token = self.refresh_token.payload.get('jti')
        check_revoke = BlacklistedToken.objects.filter(
            token__jti=jti_token).exists()

        self.assertTrue(check_revoke)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_user_with_invalid_refresh_token(self):
        response = self.make_logout_post_request(cookie_value='wrong_token')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_user_without_refresh_token(self):
        response = self.make_logout_post_request(cookie_enable=False)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
