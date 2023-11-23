from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from users.models import User
from http.cookies import SimpleCookie
from django.http import HttpResponse
from datetime import timedelta
from decouple import config
import time
import jwt


class UserSessionRegisterTests(APITestCase):
    """
    Classe específica para testar a rota de registro de usuários.

    ```
    from users.views import Register
    ```
    """

    def make_register_post_request(self, access_token: str | None = None, provider: str | None = None) -> HttpResponse:
        """
        Método para fazer uma requisição POST para a rota de registro de usuários.

        Args:
            access_token (str | None): Token de acesso do usuário.
            provider (str | None): Provedor de autenticação do usuário.

        Returns:
            response (HttpResponse): Resposta do servidor.

        Observações:
            - Se o token de acesso for None, será usado um token mock.
        """

        if access_token == None:
            access_token = config('GOOGLE_OAUTH2_MOCK_TOKEN')

        url = reverse('users:register', kwargs={'oauth2': provider})
        info = {
            'access_token': access_token
        }

        return self.client.post(url, info, format='json')

    def test_google_register_with_invalid_token(self) -> None:
        """
        Testa o registro de um usuário com um token inválido.

        Testes:
            - Mensagem de erro.
            - Status code (400 BAD REQUEST).
        """

        response = self.make_register_post_request(
            access_token='wrong_token',
            provider='google'
        )

        self.assertEqual(response.data.get('errors'), 'Invalid token')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_google_register_with_empty_token(self) -> None:
        """
        Testa o registro de um usuário com um token vazio.

        Testes:
            - Mensagem de erro.
            - Status code (400 BAD REQUEST).
        """

        response = self.make_register_post_request(
            access_token='',
            provider='google'
        )

        self.assertEqual(response.data.get('errors'), 'Invalid token')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_google_register_with_valid_token(self) -> None:
        """
        Testa o registro de um usuário com um token válido.

        Testes:
            - Usuário criado ou acessado.
            - Nome do usuário.
            - Sobrenome do usuário.
            - E-mail do usuário.
            - Status code (200 OK).
        """

        response = self.make_register_post_request(
            provider='google'
        )

        users = User.objects.all()
        self.assertEqual(len(users), 1)

        created_user = users.get(email='user@email.com')
        self.assertEqual(created_user.first_name, 'given_name')
        self.assertEqual(created_user.last_name, 'family_name')
        self.assertEqual(created_user.picture_url, 'https://photo.aqui.com')
        self.assertEqual(created_user.email, 'user@email.com')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_with_invalid_provider(self) -> None:
        """
        Testa o registro de um usuário com um provedor inválido.

        Testes:
            - Mensagem de erro.
            - Status code (400 BAD REQUEST).
        """

        provider = 'wrong_provider'
        response = self.make_register_post_request(
            access_token='token',
            provider=provider
        )

        erros = response.data.get('errors')
        self.assertEqual(erros, f'Invalid provider {provider}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_google_register_refresh_cookie_when_valid_token(self) -> None:
        """
        Testa o refresh cookie quando o token de registro de usuário é válido.

        Testes:
            - Refresh cookie.
            - Tempo de vida do cookie.
            - HttpOnly.
            - Secure.
            - Samesite.
        """

        response = self.make_register_post_request(
            provider='google'
        )

        refresh_cookie = response.cookies.get('refresh')
        max_age = 30 * 24 * 60 * 60  # 30 days in seconds
        self.assertFalse("refresh" in response.data)
        self.assertEqual(refresh_cookie.get('max-age'), max_age)
        self.assertTrue(refresh_cookie.get('httponly'))
        self.assertTrue(refresh_cookie.get('secure'))
        self.assertEqual(refresh_cookie.get('samesite'), "Lax")

    def test_google_register_refresh_cookie_when_invalid_token(self) -> None:
        """
        Testa o refresh cookie quando o token de registro de usuário é inválido.

        Testes:
            - Refresh cookie não existe.
            - Refresh cookie não está no corpo da resposta.
        """

        response = self.make_register_post_request(
            access_token='wrong_token',
            provider='google'
        )

        self.assertFalse("refresh" in response.cookies)
        self.assertFalse("refresh" in response.data)


class UserSessionLoginTests(APITestCase):
    """
    Classe específica para testar a rota de login de usuários.

    ```
    from users.views import RefreshJWTView
    ```
    """

    def setUp(self) -> None:
        """
        Método para criar um usuário para os testes.
        """

        self.user, _ = User.objects.get_or_create(
            first_name="test",
            last_name="banana",
            picture_url="https://photo.aqui.com",
            email="uiui@pichuruco.com",
        )
        self.user.save()

    def make_login_post_request(self, cookie_enable: bool = True, cookie_expired: bool = False, cookie_value: str | None = None) -> HttpResponse:
        """
        Método para fazer uma requisição POST para a rota de login de usuários.

        Args:
            cookie_enable (bool): Habilita o uso de cookies.
            cookie_expired (bool): Habilita o cookie expirado.
            cookie_value (str | None): Valor do cookie.

        Returns:
            response (HttpResponse): Resposta do servidor.
        """

        if cookie_enable:
            refresh_token = TokenObtainPairSerializer.get_token(self.user)

            if cookie_expired:
                refresh_token.set_exp(lifetime=timedelta(days=0))

            self.client.cookies = SimpleCookie(
                {'refresh': refresh_token if not cookie_value else cookie_value}
            )

        url = reverse('users:login')
        return self.client.post(url, {}, format='json')

    def test_user_login_with_invalid_token(self) -> None:
        """
        Testa o login de um usuário com um token inválido.

        Testes:
            - Status code (401 UNAUTHORIZED).
        """

        response = self.make_login_post_request(cookie_value='wrong_token')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_login_with_valid_token(self) -> None:
        """
        Testa o login de um usuário com um token válido.

        Testes:
            - Status code (200 OK).
            - Nome do usuário.
            - Sobrenome do usuário.
            - E-mail do usuário.
        """

        response = self.make_login_post_request()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], self.user.first_name)
        self.assertEqual(response.data['last_name'], self.user.last_name)
        self.assertEqual(response.data['picture_url'], self.user.picture_url)
        self.assertEqual(response.data['email'], self.user.email)

    def test_user_login_access_token(self) -> None:
        """
        Testa access token do usuário com um token válido.

        Testes:
            - Access token no corpo da resposta.
            - Tempo de vida do access token.
        """

        response = self.make_login_post_request()

        access_token = response.data.get('access')
        decoded_token = jwt.decode(
            access_token,
            config('DJANGO_SECRET_KEY'),
            algorithms=["HS256"],
        )

        def check_in_range(decoded_token):
            current_time = int(time.time())
            seconds_access_token = 1 * 24 * 60 * 60  # 1 day in seconds
            expected_expiration = current_time + seconds_access_token

            real_expiration = decoded_token.get('exp')

            lower = real_expiration <= expected_expiration + 10
            higher = expected_expiration - 10 <= real_expiration

            return lower and higher

        self.assertTrue(check_in_range(decoded_token))
        self.assertTrue('access' in response.data)

    def test_user_login_without_refresh_token(self) -> None:
        """
        Testa o login de um usuário sem o refresh token.

        Testes:
            - Código de erro.
            - Mensagem de erro.
            - Status code (401 UNAUTHORIZED).
        """

        response = self.make_login_post_request(cookie_enable=False)

        self.assertEqual(response.data.get('detail').code, 'not_authenticated')
        self.assertEqual(response.data.get('detail'), 'Refresh cookie error.')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_login_with_expired_cookie(self) -> None:
        """
        Testa o login de um usuário com um cookie expirado.

        Testes:
            - Código de erro.
            - Mensagem de erro.
            - Status code (401 UNAUTHORIZED).
        """

        response = self.make_login_post_request(cookie_expired=True)

        self.assertEqual(response.data.get('code'), 'token_not_valid')
        self.assertEqual(response.data.get('detail'), 'Token is invalid or expired')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


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

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_user_without_refresh_token(self):
        response = self.make_logout_post_request(cookie_enable=False)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
