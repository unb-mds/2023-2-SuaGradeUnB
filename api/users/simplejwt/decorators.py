from django.conf import settings
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
import functools


def move_refresh_token_to_cookie(view_func: callable) -> callable:

    @functools.wraps(view_func)
    def wrapper(request: Request, *args, **kwargs) -> Response:
        response = view_func(request, *args, **kwargs)

        if (response.status_code == status.HTTP_200_OK or response.status_code == status.HTTP_201_CREATED):
            jwt_settings = settings.SIMPLE_JWT
            refresh_token = response.data.pop('refresh')
            response.set_cookie(key="refresh", value=refresh_token,
                                max_age=jwt_settings["REFRESH_TOKEN_LIFETIME"],
                                secure=jwt_settings["REFRESH_TOKEN_SECURE"],
                                httponly=True, samesite="Lax")
        return response
    return wrapper
