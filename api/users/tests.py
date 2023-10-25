from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from http.cookies import SimpleCookie
from datetime import timedelta

class UserSessionRegisterTests(APITestCase):
    
    def test_register_with_invalid_token(self):
        url = reverse('users:register', kwargs={'oauth2': 'google'})
        info = {
            'access_token': 'wrong_token'
        } 
        response = self.client.post(url, info, format='json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 
        
class UserSessionLoginTests(APITestCase):
    
    url = reverse('users:login')
    
    def setUp(self):
        self.user, created = User.objects.get_or_create(
            first_name="test",
            last_name="banana",
            email="uiui@pichuruco.com",
        )
        self.user.save()
    
    def make_refresh_jwt_post_request(self, cookie_enable=True, cookie_expired=False, cookie_value=None):
        if cookie_enable:
            refresh_token = TokenObtainPairSerializer.get_token(self.user)

            if cookie_expired:
                refresh_token.set_exp(lifetime=timedelta(days=0))

            self.client.cookies = SimpleCookie({'refresh': refresh_token if not cookie_value else cookie_value})

        return self.client.post(self.url, {}, format='json')

    def test_user_login_with_invalid_token(self):
        response = self.make_refresh_jwt_post_request(cookie_value='wrong_token')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_login_with_valid_token(self):
        response = self.make_refresh_jwt_post_request()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], self.user.first_name)
        self.assertEqual(response.data['last_name'], self.user.last_name)
        self.assertEqual(response.data['email'], self.user.email)        
        