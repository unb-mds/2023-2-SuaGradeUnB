from rest_framework import status, exceptions, response, request
from rest_framework_simplejwt import exceptions as jwt_exceptions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from users.backends.utils import get_backend
from users.simplejwt.decorators import move_refresh_token_to_cookie
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.swagger import Errors


class Register(TokenObtainPairView):

    GOOGLE_HELP_URL = "https://developers.google.com/identity/protocols/oauth2/javascript-implicit-flow?hl=pt-br"

    @swagger_auto_schema(
        operation_description="""Registra um novo usuário no sistema, ou retorna os dados caso o mesmo já exista.
        O header da resposta acompanha o token de `refresh` nos cookies no seguinte formato:

        headers = {
            "Set-Cookie": "refresh=<refresh-token>; Secure; HttpOnly; SameSite=Lax; Expires=<expires-date>"
        }
        """,
        security=[],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'access_token': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description=f"""Token de acesso provido pelo provedor \n de autenticação Google.
                    Os passos para obter o token podem ser encontrados [aqui]({GOOGLE_HELP_URL})"""
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
            **Errors([400]).retrieve_erros()
        }
    )
    @move_refresh_token_to_cookie
    def post(self, request: request.Request, *args, **kwargs) -> response.Response:
        token = request.data.get('access_token')

        backend = get_backend(kwargs['oauth2'])
        if not backend:
            return response.Response(
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

            return response.Response(data, status.HTTP_200_OK)

        return response.Response(
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


class HandlePostErrorMixin():

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except jwt_exceptions.TokenError:
            return response.Response({
                "errors": "Token is invalid or expired"
            }, status=status.HTTP_400_BAD_REQUEST)

        return response.Response(serializer.validated_data, status=status.HTTP_200_OK)


class RefreshJWTView(HandlePostErrorMixin, HandleRefreshMixin, TokenRefreshView):

    @swagger_auto_schema(
        operation_description="""Atualiza o token de acesso JWT, caso o token de `refresh` esteja presente nos **request cookies**.
        O header da resposta acompanha o novo token de `refresh` nos cookies no seguinte formato:

        // Request
        headers = {
            Cookie: "refresh=<refresh-token>"
        }

        // Response
        headers = {
            "Set-Cookie": "refresh=<refresh-token>; Secure; HttpOnly; SameSite=Lax; Expires=<expires-date>"
        }
        """,
        security=[],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
        ),
        responses={
            200: openapi.Response('OK', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'access': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Token de acesso JWT'
                    ),
                }
            )),
            **Errors([400]).retrieve_erros()
        }
    )
    @move_refresh_token_to_cookie
    def post(self, request, *args, **kwargs):
        request = self.handle(request)
        return super().post(request, *args, **kwargs)


class BlacklistJWTView(HandlePostErrorMixin, HandleRefreshMixin, TokenBlacklistView):

    @swagger_auto_schema(
        operation_description="""Revoga o Token de acesso JWT, caso o token de `refresh` esteja presente nos **request cookies**.
            
            // Request
            headers = {
                Cookie: "refresh=<refresh-token>"
            }
            """,
        security=[],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
        ),
        responses={
            200: openapi.Response('OK', openapi.Schema(
                type=openapi.TYPE_OBJECT,
            )),
            **Errors([400]).retrieve_erros()
        }
    )
    def post(self, request, *args, **kwargs):
        request = self.handle(request)
        return super().post(request, *args, **kwargs)
