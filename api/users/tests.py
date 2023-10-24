from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

class UserSessionLoginTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.token = "test_token"
        
    def verify_token(self, token):
        self.assertEqual(token, self.token)
        
    def test_login(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.post(reverse('users:login'), {'access_token': self.token})
        self.assertEqual(response.status_code, 200)
        self.verify_token(response.data['access'])
    
    
    