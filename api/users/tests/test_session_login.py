from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.models import User
from http.cookies import SimpleCookie
from django.http import HttpResponse
from datetime import timedelta
from decouple import config
import time
import jwt

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

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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

        self.assertEqual(response.data.get('errors'), 'Token is invalid or expired')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
