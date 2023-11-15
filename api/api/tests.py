from django.test import TestCase
from rest_framework.test import APITestCase
from .models import Department, Discipline, Class
from utils.db_handler import get_or_create_department, get_or_create_discipline, create_class
from .views import Search, ERROR_MESSAGE
import json


class DisciplineModelsTest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(
            code='INF',
            year="2023",
            period="2"
        )

        self.discipline = Discipline.objects.create(
            name='Métodos de Desenvolvimento de Software',
            code='MDS1010',
            department=self.department
        )
        self._class = Class.objects.create(
            workload=60,
            teachers=['Professor 1', 'Professor 2'],
            classroom='MOCAP',
            schedule='46M34',
            days=['Quarta-Feira 10:00 às 11:50', 'Sexta-Feira 10:00 às 11:50'],
            _class="1",
            discipline=self.discipline
        )

    def test_create_discipline(self):
        self.assertEqual(self.discipline.name,
                         'Métodos de Desenvolvimento de Software')
        self.assertEqual(self.discipline.code, 'MDS1010')
        self.assertEqual(self.discipline.department, self.department)

    def test_create_class(self):
        self.assertEqual(self._class.workload, 60)
        self.assertEqual(self._class.teachers, ['Professor 1', 'Professor 2'])
        self.assertEqual(self._class.classroom, 'MOCAP')
        self.assertEqual(self._class.schedule, '46M34')
        self.assertEqual(self._class.days, [
                         'Quarta-Feira 10:00 às 11:50', 'Sexta-Feira 10:00 às 11:50'])
        self.assertEqual(self._class._class, "1")
        self.assertEqual(self._class.discipline, self.discipline)

    def test_create_department(self):
        self.assertEqual(self.department.code, 'INF')
        self.assertEqual(self.department.year, '2023')
        self.assertEqual(self.department.period, '2')

    def test_str_method_of_discipline(self):
        self.assertEqual(str(self.discipline), self.discipline.name)

    def test_str_method_of_class(self):
        self.assertEqual(str(self._class), self._class._class)

    def test_str_method_of_department(self):
        self.assertEqual(str(self.department), self.department.code)


class Testsad(APITestCase):
    def setUp(self) -> None:
        self.department = get_or_create_department(
            code='518', year='2023', period='2')
        self.discipline_1 = get_or_create_discipline(
            name='CÁLCULO 1', code='MAT518', department=self.department)
        self.discipline_2 = get_or_create_discipline(
            name='CÁLCULO 2', code='MAT519', department=self.department)
        self._class_1 = create_class(workload=60, teachers=['RICARDO FRAGELLI'], classroom='MOCAP', schedule='46M34',
                                     days=['Quarta-Feira 10:00 às 11:50', 'Sexta-Feira 10:00 às 11:50'], _class="1", discipline=self.discipline_1)
        self._class_2 = create_class(workload=60, teachers=['VINICIUS RISPOLI'], classroom='S1', schedule='24M34', days=[
                                     'Segunda-Feira 10:00 às 11:50', 'Quarta-Feira 10:00 às 11:50'], _class="1", discipline=self.discipline_2)

    def test_with_complete_correct_search(self):
        """
        Testa a busca por disciplinas com o nome completo e todos os parâmetros corretos

        Testes:
        - Status code (200 OK)
        - Quantidade de disciplinas retornadas
        - Código do departamento
        - Nome da disciplina
        - Professores da disciplina
        """
        response_for_discipline_1 = self.client.get(
            '/courses/?search=calculo+1&year=2023&period=2')
        response_for_discipline_2 = self.client.get(
            '/courses/?search=calculo+2&year=2023&period=2')
        content_1 = json.loads(response_for_discipline_1.content)
        content_2 = json.loads(response_for_discipline_2.content)

        # Testes da disciplina 1
        self.assertEqual(response_for_discipline_1.status_code, 200)
        self.assertEqual(len(content_1), 1)
        self.assertEqual(content_1[0]['department']
                         ['code'], self.department.code)
        self.assertEqual(content_1[0]['name'], self.discipline_1.name)
        self.assertEqual(content_1[0]['classes'][0]
                         ['teachers'], self._class_1.teachers)

        # Testes da disciplina 2
        self.assertEqual(response_for_discipline_2.status_code, 200)
        self.assertEqual(len(content_2), 1)
        self.assertEqual(content_2[0]['department']
                         ['code'], self.department.code)
        self.assertEqual(content_2[0]['name'], self.discipline_2.name)
        self.assertEqual(content_2[0]['classes'][0]
                         ['teachers'], self._class_2.teachers)

    def test_with_incomplete_correct_search(self):
        """
        Testa a busca por disciplinas com nome incompleto e todos os parâmetros corretos

        Testes:
        - Status code (200 OK)
        - Quantidade de disciplinas retornadas
        - Código do departamento
        - Nome da disciplina
        - Professores da disciplina
        """
        response_for_disciplines = self.client.get(
            '/courses/?search=calculo&year=2023&period=2')
        content = json.loads(response_for_disciplines.content)

        # Testes da disciplina 1
        self.assertEqual(response_for_disciplines.status_code, 200)
        self.assertEqual(len(content), 2)
        self.assertEqual(content[0]['department']
                         ['code'], self.department.code)
        self.assertEqual(content[0]['name'], self.discipline_1.name)
        self.assertEqual(content[0]['classes'][0]
                         ['teachers'], self._class_1.teachers)
        # Testes da disciplina 2
        self.assertEqual(content[1]['department']
                         ['code'], self.department.code)
        self.assertEqual(content[1]['name'], self.discipline_2.name)
        self.assertEqual(content[1]['classes'][0]
                         ['teachers'], self._class_2.teachers)

    def test_with_bad_url_search_missing_year(self):
        """
        Testa a busca por disciplinas sem os parâmetros de ano, como None e como string vazia
        Testes:
        - Status code (400 BAD REQUEST)
        - Quantidade de resposta no JSON
        - Mensagem de erro
        """
        response_1 = self.client.get(
            '/courses/?search=calculo&')
        response_2 = self.client.get(
            '/courses/?search=calculo&year=&period=2')
        content_1 = json.loads(response_1.content)
        content_2 = json.loads(response_2.content)

        # Testes com ano None
        self.assertEqual(response_1.status_code, 400)
        self.assertEqual(len(content_1), 1)
        self.assertEqual(content_1['errors'], ERROR_MESSAGE)

        # Testes com ano string vazia
        self.assertEqual(response_2.status_code, 400)
        self.assertEqual(len(content_2), 1)
        self.assertEqual(content_2['errors'], ERROR_MESSAGE)

    def test_with_bad_url_search_missing_period(self):
        """
        Testa a busca por disciplinas sem os parâmetros de período, como None e como string vazia
        Testes:
        - Status code (400 BAD REQUEST)
        - Quantidade de resposta no JSON
        - Mensagem de erro
        """
        response_1 = self.client.get(
            '/courses/?search=calculo&year=2023')
        response_2 = self.client.get(
            '/courses/?search=calculo&year=2023&period=')
        content_1 = json.loads(response_1.content)
        content_2 = json.loads(response_2.content)

        # Testes com período None
        self.assertEqual(response_1.status_code, 400)
        self.assertEqual(len(content_1), 1)
        self.assertEqual(content_1['errors'], ERROR_MESSAGE)

        # Testes com período string vazia
        self.assertEqual(response_2.status_code, 400)
        self.assertEqual(len(content_2), 1)
        self.assertEqual(content_2['errors'], ERROR_MESSAGE)

    def test_with_bad_url_search_missing_name(self):
        """
        Testa a busca por disciplinas sem os parâmetros de nome, como None e como string vazia
        Testes:
        - Status code (400 BAD REQUEST)
        - Quantidade de resposta no JSON
        - Mensagem de erro
        """
        response_1 = self.client.get(
            '/courses/?year=2023&period=2')
        response_2 = self.client.get(
            '/courses/?search=&year=2023&period=2')
        content_1 = json.loads(response_1.content)
        content_2 = json.loads(response_2.content)

        # Testes com nome None
        self.assertEqual(response_1.status_code, 400)
        self.assertEqual(len(content_1), 1)
        self.assertEqual(content_1['errors'], ERROR_MESSAGE)

        # Testes com nome string vazia
        self.assertEqual(response_2.status_code, 400)
        self.assertEqual(len(content_2), 1)
        self.assertEqual(content_2['errors'], ERROR_MESSAGE)

    def test_with_bad_url_search_missing_all_parameters(self):
        """
        Testa a busca por disciplinas sem nenhum parâmetro, como None e como string vazia
        Testes:
        - Status code (400 BAD REQUEST)
        - Quantidade de resposta no JSON
        - Mensagem de erro
        """
        response_1 = self.client.get('/courses/')
        response_2 = self.client.get('/courses/?search=&year=&period=')
        content_1 = json.loads(response_1.content)
        content_2 = json.loads(response_2.content)

        # Testes com todos os parâmetros None
        self.assertEqual(response_1.status_code, 400)
        self.assertEqual(len(content_1), 1)
        self.assertEqual(content_1['errors'], ERROR_MESSAGE)

        # Testes com todos os parâmetros string vazia
        self.assertEqual(response_2.status_code, 400)
        self.assertEqual(len(content_2), 1)
        self.assertEqual(content_2['errors'], ERROR_MESSAGE)
