import requests
from users.models import User
from decouple import config
from requests import Response
from rest_framework import status


class GoogleOAuth2:
    GOOGLE_OAUTH2_PROVIDER = 'https://www.googleapis.com/oauth2/v3'

    @classmethod
    def get_user_data(cls, access_token: str) -> dict | None:
        if not access_token:
            return None

        user_info_url = cls.GOOGLE_OAUTH2_PROVIDER + '/userinfo'
        params = {'access_token': access_token}

        try:
            response = Response()
            response.status_code = status.HTTP_400_BAD_REQUEST 
            response.headers = {'Content-Type': 'application/json'}

            if access_token != config('GOOGLE_OAUTH2_MOCK_TOKEN'):
                response = requests.get(user_info_url, params=params)
            else:
                response._content = b'''{
                    "given_name": "given_name",
                    "family_name": "family_name",
                    "picture": "https://photo.aqui.com",
                    "email": "user@email.com"
                }'''
                response.status_code = status.HTTP_200_OK

            if response.status_code == 200:
                user_data = response.json()
                return user_data
            else:
                return None
        except requests.exceptions.RequestException as e:
            return None

    @staticmethod
    def do_auth(user_data: dict) -> User | None:
        user, created = User.objects.get_or_create(
            first_name=user_data['given_name'],
            email=user_data['email'],
        )

        if user_data.get('family_name'):
            user.last_name = user_data['family_name']
        
        if user_data.get('picture'):
            user.picture_url = user_data['picture']

        if created:
            user.save()

        return user
