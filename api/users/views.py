from rest_framework import status
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from users.backends.utils import get_backend
from users.simplejwt.decorators import move_refresh_token_to_cookie


class Register(TokenObtainPairView):

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
