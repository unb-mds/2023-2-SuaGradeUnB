from rest_framework.test import APITestCase
from .web_scraping import get_list_of_departments
from django.urls import reverse


class WebScrapingTest(APITestCase):

    url = reverse('utils:departments')

    def test_get_list_of_departments(self):
        response = self.client.get(self.url)

        departments = get_list_of_departments(response)
        self.assertEqual(type(list()), type(departments))
        if len(departments):
            self.assertEqual(type(str()), type(departments[0]))
