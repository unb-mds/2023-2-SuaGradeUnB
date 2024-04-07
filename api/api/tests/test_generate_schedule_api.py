from rest_framework.test import APITestCase, APIRequestFactory
from utils.db_handler import get_or_create_department, get_or_create_discipline, create_class
from random import randint
import json


class TestGenerateScheduleAPI(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.content_type = 'application/json'
        self.api_url = '/courses/schedules/generate/'
        self.department = get_or_create_department(
            code='518', name='Departamento de Matemática e Estatística', year='2023', period='2')
        self.discipline = get_or_create_discipline(
            name='CÁLCULO 1', code='MAT518', department=self.department)
        self.class_1 = create_class(teachers=['RICARDO FRAGELLI'], classroom='S9', schedule='46M34', days=[
                                    'Quarta-Feira 10:00 às 11:50', 'Sexta-Feira 10:00 às 11:50'], _class="1", special_dates=[], discipline=self.discipline)
        self.class_2 = create_class(teachers=['VINICIUS RISPOLI'], classroom='S1', schedule='24M34', days=[
                                    'Segunda-Feira 10:00 às 11:50', 'Quarta-Feira 10:00 às 11:50'], _class="2", special_dates=[], discipline=self.discipline)
        self.discipline_2 = get_or_create_discipline(
            name='CÁLCULO 2', code='MAT519', department=self.department)
        self.class_3 = create_class(teachers=['LUIZA YOKO'], classroom='S1', schedule='56M23', days=[
                                    'Segunda-Feira 10:00 às 11:50', 'Quarta-Feira 10:00 às 11:50'], _class="1", special_dates=[], discipline=self.discipline_2)
        self.class_4 = create_class(teachers=['Tatiana'], classroom='S1', schedule='7M1234', days=[
                                    'Sábado 08:00 às 11:50'], _class="2", special_dates=[], discipline=self.discipline_2)

    def test_with_correct_parameters(self):
        """
        Testa a geração de horários com todos os parâmetros corretos
        Os parâmetros enviados permitem que pelo menos uma solução seja encontrada
        """
        body = json.dumps({
            'preference': [3, 2, 1],
            'classes': [self.class_1.id, self.class_2.id, self.class_3.id, self.class_4.id]
        })

        response = self.client.post(
            self.api_url, body, content_type=self.content_type)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data["schedules"]) > 0)

    def test_with_conflicting_classes(self):
        """
        Testa a geração de horários com classes conflitantes
        """
        body = json.dumps({
            'preference': [3, 2, 1],
            'classes': [self.class_1.id, self.class_3.id]
        })

        response = self.client.post(
            self.api_url, body, content_type=self.content_type)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(len(response.data["schedules"]))

    def test_with_invalid_class(self):
        """
        Testa a geração de horários com uma classe inválida
        """

        classes_ids = [self.class_1.id, self.class_2.id,
                       self.class_3.id, self.class_4.id]
        random_id = randint(1, 10000)

        while (random_id in classes_ids):  # pragma: no cover
            random_id = randint(1, 10000)

        body = json.dumps({
            'preference': [3, 2, 1],
            'classes': classes_ids + [random_id]
        })

        response = self.client.post(
            self.api_url, body, content_type=self.content_type)

        self.assertEqual(response.status_code, 400)

    def test_with_invalid_preference(self):
        """
        Testa a geração de horários com uma preferência inválida
        """
        body = json.dumps({
            'preference': [3, 2, 1, 4],
            'classes': [self.class_1.id, self.class_2.id, self.class_3.id, self.class_4.id]
        })

        response = self.client.post(
            self.api_url, body, content_type=self.content_type)

        self.assertEqual(response.status_code, 400)

    def test_with_invalid_preference_type(self):
        """
        Testa a geração de horários com uma preferência inválida (tipo)
        """
        body = json.dumps({
            'preference': [3, 2, '1'],
            'classes': [self.class_1.id, self.class_2.id, self.class_3.id, self.class_4.id]
        })

        response = self.client.post(
            self.api_url, body, content_type=self.content_type)

        self.assertEqual(response.status_code, 400)

    def test_with_no_classes(self):
        """
        Testa a geração de horários sem classes
        """
        body = json.dumps({
            'classes': []
        })

        response = self.client.post(
            self.api_url, body, content_type=self.content_type)

        self.assertEqual(response.status_code, 400)

    def test_with_no_preference(self):
        """
        Testa a geração de horários sem preferência
        """
        body = json.dumps({
            'classes': [self.class_1.id]
        })

        response = self.client.post(
            self.api_url, body, content_type=self.content_type)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data["schedules"]) > 0)
