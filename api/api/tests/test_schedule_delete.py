from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from utils import db_handler as dbh

from users.models import User

import json


class TestDeleteSchedules(APITestCase):
    def setUp(self):
        self.department = dbh.get_or_create_department(
            '518', 'Departamento de Matemática e Estatística', '2023', '2')
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

        self.url = "api:delete-schedule"
        self.content_type = 'application/json'

        self.data = self.client.post(
            reverse('api:generate-schedules'), body, content_type=self.content_type).data
        self.schedules = self.data.get('schedules')

        self.schedule_json = json.dumps(self.schedules[0])

        self.headers = {
            'Authorization': 'Bearer ' + str(self.access_token)
        }

    def save_schedule(self):
        self.client.post(reverse('api:schedules'),
                         self.schedule_json, content_type=self.content_type, headers=self.headers)

    def get_user_schedules(self):
        return self.client.get(
            reverse('api:schedules'), headers=self.headers)

    def test_delete_non_existent_schedule(self):
        """
        Testa a deleção de uma grade horária que não existe
        """

        content = self.client.delete(
            reverse(self.url, kwargs={'id': 1}), headers=self.headers)

        self.assertEqual(content.status_code, 400)

    def test_delete_schedule(self):
        """
        Testa a deleção de uma grade horária
        """

        self.save_schedule()

        user_schedules = self.get_user_schedules().data
        schedule_id = user_schedules[0].get('id')

        content = self.client.delete(
            reverse(self.url, kwargs={'id': schedule_id}), headers=self.headers)

        self.assertEqual(content.status_code, 204)
        self.assertEqual(len(self.get_user_schedules().data), 0)

    def test_delete_schedule_with_invalid_token(self):
        """
        Testa a deleção de uma grade horária com um token inválido
        """

        content = self.client.delete(
            reverse(self.url, kwargs={'id': 12}), headers={'Authorization': 'Bearer ' + str('invalid_token')})

        self.assertEqual(content.status_code, 403)
