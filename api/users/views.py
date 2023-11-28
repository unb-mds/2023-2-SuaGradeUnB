from rest_framework import status
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from users.backends.utils import get_backend
from users.simplejwt.decorators import move_refresh_token_to_cookie
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class Register(TokenObtainPairView):

    @swagger_auto_schema(
        operation_description="""Registra um novo usuário no sistema, ou retorna os dados caso o mesmo já exista.
        O header da resposta acompanha o token de `refresh` nos cookies no seguinte formato:

        headers = {
            "Set-Cookie": "refresh=<refresh-token>; Secure; HttpOnly; SameSite=Lax; Expires=<expires-date>"
        }
        """,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'access_token': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Token de acesso provido pelo provedor \n de autenticação (Google, Facebook, etc)'
                ),
            }
        ),
        responses={
            200: openapi.Response('OK', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'access': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Token de acesso JWT'
                    ),
                    'first_name': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Primeiro nome do usuário'
                    ),
                    'last_name': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Último nome do usuário'
                    ),
                    'picture_url': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='URL da foto do usuário'
                    ),
                    'email': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Email do usuário'
                    ),
                }
            )),
            400: openapi.Response('Bad Request', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'errors': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Mensagem de erro'
                    ),
                }
            )),
        }
    )
    @move_refresh_token_to_cookie
    def post(self, request: Request, *args, **kwargs) -> Response:
        token = request.data.get('access_token')

        backend = get_backend(kwargs['oauth2'])
        if not backend:
            return Response(
                {
                    'errors': f'Invalid provider {kwargs["oauth2"]}'
                }, status=status.HTTP_400_BAD_REQUEST)

        user_data = backend.get_user_data(token)
        if user_data:
            user = backend.do_auth(user_data)

            serializer = self.get_serializer()
            refresh = serializer.get_token(user)
            data = {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'first_name': user.first_name,
                'last_name': user.last_name,
                'picture_url': user.picture_url,
                'email': user.email,
            }

            return Response(data, status.HTTP_200_OK)

        return Response(
            {
                'errors': 'Invalid token'
            }, status.HTTP_400_BAD_REQUEST)


class HandleRefreshMixin:

    def handle(self, request):
        try:
            request.data['refresh'] = request.COOKIES['refresh']
        except KeyError:
            raise exceptions.NotAuthenticated('Refresh cookie error.')

        return request


class RefreshJWTView(TokenRefreshView, HandleRefreshMixin):

    @move_refresh_token_to_cookie
    def post(self, request, *args, **kwargs):
        request = self.handle(request)
        return super().post(request, *args, **kwargs)


class BlacklistJWTView(TokenBlacklistView, HandleRefreshMixin):

    def post(self, request, *args, **kwargs):
        request = self.handle(request)
        return super().post(request, *args, **kwargs)
