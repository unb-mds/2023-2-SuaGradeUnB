from rest_framework.test import APITestCase
from utils import sessions as sns


class TestYearPeriodAPI(APITestCase):

    def test_year_period(self):
        """
        Testa se a API retorna o ano/periodo atual e o próximo ano/periodo

        Testes:
        - Status code (200 OK)
        - Dados retornados (ano/periodo atual e próximo ano/periodo)
        """

        response = self.client.get('/courses/year-period/')
        year, period = sns.get_current_year_and_period()
        next_year, next_period = sns.get_next_period()

        expected_data = {
            'year/period': [f'{year}/{period}', f'{next_year}/{next_period}'],
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)
