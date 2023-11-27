from rest_framework.test import APITestCase
from utils.db_handler import get_or_create_department, get_or_create_discipline, create_class
from api.views import ERROR_MESSAGE, ERROR_MESSAGE_SEARCH_LENGTH
import json

class TestSearchAPI(APITestCase):
    def setUp(self) -> None:
        self.department = get_or_create_department(
            code='518', year='2023', period='2')
        self.discipline_1 = get_or_create_discipline(
            name='CÁLCULO 1', code='MAT518', department=self.department)
        self.discipline_2 = get_or_create_discipline(
            name='CÁLCULO 2', code='MAT519', department=self.department)
        self._class_1 = create_class(teachers=['RICARDO FRAGELLI'], classroom='MOCAP', schedule='46M34',
                                     days=['Quarta-Feira 10:00 às 11:50', 'Sexta-Feira 10:00 às 11:50'], _class="1", special_dates=[], discipline=self.discipline_1)
        self._class_2 = create_class(teachers=['VINICIUS RISPOLI'], classroom='S1', schedule='24M34', days=[
                                     'Segunda-Feira 10:00 às 11:50', 'Quarta-Feira 10:00 às 11:50'], _class="1", special_dates=[], discipline=self.discipline_2)

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

    def test_with_code_search(self):
        """
        Testa a busca por disciplinas através do código da matéria
        Testes:
        - Status code (200 OK)
        - Quantidade de disciplinas retornadas
        """

        response_for_discipline_1 = self.client.get(
            '/courses/?search=MAT518&year=2023&period=2')
        response_for_discipline_2 = self.client.get(
            '/courses/?search=MAT519&year=2023&period=2')
        content_1 = json.loads(response_for_discipline_1.content)
        content_2 = json.loads(response_for_discipline_2.content)

        # Testes da disciplina 1
        self.assertEqual(response_for_discipline_1.status_code, 200)
        self.assertEqual(len(content_1), 1)

        # Testes da disciplina 2
        self.assertEqual(response_for_discipline_2.status_code, 200)
        self.assertEqual(len(content_2), 1)
    
    def test_with_code_search_spaced(self):
        """
        Testa a busca por disciplinas através do código da matéria com espaços
        Testes:
        - Status code (200 OK)
        - Quantidade de disciplinas retornadas
        """

        response_for_discipline_1 = self.client.get(
            '/courses/?search=MAT+518&year=2023&period=2')
        response_for_discipline_2 = self.client.get(
            '/courses/?search=MAT+519&year=2023&period=2')
        content_1 = json.loads(response_for_discipline_1.content)
        content_2 = json.loads(response_for_discipline_2.content)

        # Testes da disciplina 1
        self.assertEqual(response_for_discipline_1.status_code, 200)
        self.assertEqual(len(content_1), 1)

        # Testes da disciplina 2
        self.assertEqual(response_for_discipline_2.status_code, 200)
        self.assertEqual(len(content_2), 1)

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

    def test_with_only_spaces(self):
        """
        Testa a busca por disciplinas com apenas espaços nos parâmetros
        Testes:
        - Status code (400 BAD REQUEST)
        """

        response_1 = self.client.get('/courses/?search=     &year=2023&period=2')
        response_2 = self.client.get('/courses/?search=calculo&year=     &period=2')
        response_3 = self.client.get('/courses/?search=calculo&year=2023&period=     ')
        content_1 = json.loads(response_1.content)
        content_2 = json.loads(response_2.content)
        content_3 = json.loads(response_3.content)

        self.assertEqual(response_1.status_code, 400)
        self.assertEqual(len(content_1), 1)
        self.assertEqual(content_1['errors'], ERROR_MESSAGE)

        self.assertEqual(response_2.status_code, 400)
        self.assertEqual(len(content_2), 1)
        self.assertEqual(content_2['errors'], ERROR_MESSAGE)

        self.assertEqual(response_3.status_code, 400)
        self.assertEqual(len(content_3), 1)
        self.assertEqual(content_3['errors'], ERROR_MESSAGE)
        
    def test_with_insufficient_search_length(self):
        """
        Testa a busca por disciplinas com menos de 4 caracteres no parâmetro de busca
        Testes:
        - Status code (400 BAD REQUEST)
        """

        response_1 = self.client.get('/courses/?search=cal&year=2023&period=2')
        content_1 = json.loads(response_1.content)

        self.assertEqual(response_1.status_code, 400)
        self.assertEqual(len(content_1), 1)
        self.assertEqual(content_1['errors'], ERROR_MESSAGE_SEARCH_LENGTH)