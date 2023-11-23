from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from django.http import HttpResponse
from decouple import config

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
