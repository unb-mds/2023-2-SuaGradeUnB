from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from utils import db_handler as dbh

from users.models import User

import json


class TestGetSchedules(APITestCase):
    def setUp(self):
        self.department = dbh.get_or_create_department(
            '518', 'Departamento de matematica', '2023', '2')
        self.discipline = dbh.get_or_create_discipline(
            'CÁLCULO 1', 'MAT0025', self.department)
        self._class = dbh.create_class(['EDSON ALVES DA COSTA JUNIOR'], 'FGA - I8', '35T23', [
            'Terça-feira 14:00 às 15:50', 'Quinta-feira 14:00 às 15:50'], '1', [], self.discipline)

        body = json.dumps(
            {
                "classes": [self._class.id]
            }
        )

        self.user, _ = User.objects.get_or_create(
            first_name='Aroldo',
            last_name='Silva',
            picture_url='https://www.photo.com',
            email="aroldosilva@none.com"
        )
        self.user.save()

        tokens = TokenObtainPairSerializer.get_token(self.user)
        self.access_token = tokens.access_token

        self.url = reverse('api:schedules')
        self.content_type = 'application/json'

        self.data = self.client.post(
            reverse('api:generate-schedules'), body, content_type=self.content_type).data
        self.schedules = self.data.get('schedules')

        self.schedule_json = json.dumps(self.schedules[0])

        self.headers = {
            'Authorization': 'Bearer ' + str(self.access_token)
        }
        self.client.post(self.url,
                         self.schedule_json, content_type=self.content_type, headers=self.headers)

    def test_get_schedules(self):
        """
        Testa a obtenção de horários salvos
        """

        content = self.client.get(
            self.url, headers=self.headers)

        self.assertEqual(len(content.data), 1)
        self.assertEqual(content.status_code, 200)

    def test_get_schedules_with_invalid_token(self):
        """
        Testa a obtenção de horários salvos com um token inválido
        """

        content = self.client.get(
            self.url, headers={'Authorization': 'Bearer ' + str(self.access_token) + '1'})

        self.assertEqual(content.status_code, 403)
