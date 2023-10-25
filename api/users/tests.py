from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

class UserSessionLoginTests(TestCase):
    
    def setUp(self):
        self.token = "test_token"
        
    def test_verify_token(self, token="test_token"):
        self.assertEqual(token, self.token)

    def test_register_with_invalid_token(self):
        url = reverse('users:register', kwargs={'oauth2': 'google-oauth2'}) 
        response = self.client.post(url, {'access_token': self.token}) 
        self.assertNotEqual(response.status_code, status.HTTP_200_OK) 

    def test_user_login_with_invalid_token(self):
        url = reverse('users:login')
        response = self.client.post(url, {'access_token': self.token})
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

        
        