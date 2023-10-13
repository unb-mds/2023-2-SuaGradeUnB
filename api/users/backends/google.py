import requests
from users.models import User


class GoogleOAuth2:
    GOOGLE_OAUTH2_PROVIDER = 'https://www.googleapis.com/oauth2/v3'

    @classmethod
    def get_user_data(cls, access_token: str) -> dict | None:
        if not access_token:
            return None

        user_info_url = cls.GOOGLE_OAUTH2_PROVIDER + '/userinfo'
        params = {'access_token': access_token}
        
        try:
            response = requests.get(user_info_url, params=params)
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
            last_name=user_data['family_name'],
        )

        if created:
            user.email = user_data['email']
            user.save()

        return user
