from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from http.cookies import SimpleCookie
from datetime import timedelta
from decouple import config
from core.settings.base import REFRESH_TOKEN_LIFETIME


class UserSessionRegisterTests(APITestCase):

    def make_register_post_request(self, access_token=None, provider=None):
        if access_token == None:
            access_token = config('GOOGLE_OAUTH2_MOCK_TOKEN')

        url = reverse('users:register', kwargs={'oauth2': provider})
        info = {
            'access_token': access_token
        }

        return self.client.post(url, info, format='json')

    def test_google_register_with_invalid_token(self):
        response = self.make_register_post_request(
            access_token='wrong_token',
            provider='google'
        )

        self.assertEqual(response.data.get('errors'), 'Invalid token')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_google_register_with_empty_token(self):
        response = self.make_register_post_request(
            access_token='',
            provider='google'
        )

        self.assertEqual(response.data.get('errors'), 'Invalid token')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_google_register_with_valid_token(self):
        response = self.make_register_post_request(
            provider='google'
        )

        users = User.objects.all()
        self.assertEqual(len(users), 1)

        created_user = users.get(email='user@email.com')
        self.assertEqual(created_user.first_name, 'given_name')
        self.assertEqual(created_user.last_name, 'family_name')
        self.assertEqual(created_user.email, 'user@email.com')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_with_invalid_provider(self):
        provider = 'wrong_provider'
        response = self.make_register_post_request(
            access_token='token',
            provider=provider
        )

        erros = response.data.get('errors')
        self.assertEqual(erros, f'Invalid provider {provider}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_google_register_refresh_cookie_when_valid_token(self):
        response = self.make_register_post_request(
            provider='google'
        )

        refresh_cookie = response.cookies.get('refresh')
        max_age = REFRESH_TOKEN_LIFETIME.total_seconds()
        self.assertFalse("refresh" in response.data)
        self.assertEqual(refresh_cookie.get('max-age'), max_age)
        self.assertTrue(refresh_cookie.get('httponly'))
        self.assertTrue(refresh_cookie.get('secure'))
        self.assertEqual(refresh_cookie.get('samesite'), "Lax")

    def test_google_register_refresh_cookie_when_invalid_token(self):
        response = self.make_register_post_request(
            access_token='wrong_token',
            provider='google'
        )

        self.assertFalse("refresh" in response.cookies)
        self.assertFalse("refresh" in response.data)


class UserSessionLoginTests(APITestCase):

    def setUp(self):
        self.user, _ = User.objects.get_or_create(
            first_name="test",
            last_name="banana",
            email="uiui@pichuruco.com",
        )
        self.user.save()

    def make_login_post_request(self, cookie_enable=True, cookie_expired=False, cookie_value=None):
        if cookie_enable:
            refresh_token = TokenObtainPairSerializer.get_token(self.user)

            if cookie_expired:
                refresh_token.set_exp(lifetime=timedelta(days=0))

            self.client.cookies = SimpleCookie(
                {'refresh': refresh_token if not cookie_value else cookie_value}
            )

        url = reverse('users:login')
        return self.client.post(url, {}, format='json')

    def test_user_login_with_invalid_token(self):
        response = self.make_login_post_request(
            cookie_value='wrong_token')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_login_with_valid_token(self):
        response = self.make_login_post_request()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], self.user.first_name)
        self.assertEqual(response.data['last_name'], self.user.last_name)
        self.assertEqual(response.data['email'], self.user.email)
