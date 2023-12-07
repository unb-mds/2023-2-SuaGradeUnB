from django.test import TestCase

from api.models import Schedule

from users.models import User

import json


class ScheduleModelsTest(TestCase):

    def setUp(self):
        self.user, _ = User.objects.get_or_create(
            first_name="test",
            last_name="banana",
            picture_url="https://photo.aqui.com",
            email="uiui@pichuruco.com",
        )
        self.user.save()

        mock_json = json.dumps([
            {'class': 1},
            {'class': 2},
        ])
        self.schedule = Schedule.objects.create(
            user=self.user,
            classes=mock_json
        )

    def test_create_schedule(self):
        """
        Testa se o schedule foi criado corretamente

        Tests:
        - Se o usuário é o mesmo que o entrega na criação
        - Se as classes são as mesmas que as entregues na criação
        """
        self.assertEqual(self.schedule.user, self.user)
        self.assertEqual(self.schedule.classes, json.dumps([
            {'class': 1},
            {'class': 2},
        ]))

    def test_str_method_of_schedule(self):
        """
        Testa se o método __str__ de Schedule retorna o json correto
        """
        self.assertEqual(str(self.schedule), json.dumps([
            {'class': 1},
            {'class': 2},
        ]))
