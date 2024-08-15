from rest_framework.test import APITestCase
from utils.db_handler import get_or_create_department, get_or_create_discipline, create_class
from api.views.views import ERROR_MESSAGE, ERROR_MESSAGE_SEARCH_LENGTH
import json


class TestSearchAPI(APITestCase):
    def setUp(self) -> None:
        self.department = get_or_create_department(
            code='518', year='2023', period='2')
        self.discipline_1 = get_or_create_discipline(
            name='CÁLCULO 1', code='MAT518', department=self.department)
        self.discipline_2 = get_or_create_discipline(
            name='CÁLCULO 2', code='MAT519', department=self.department)
        self.discipline_3 = get_or_create_discipline(
            name='ÁLGEBRA LINEAR', code='MAT520', department=self.department)
        self._class_1 = create_class(
            teachers=['RICARDO FRAGELLI'], classroom='MOCAP', schedule='46M34',
            days=['Quarta-Feira 10:00 às 11:50', 'Sexta-Feira 10:00 às 11:50'], _class="1", special_dates=[], discipline=self.discipline_1)
        self._class_2 = create_class(
            teachers=['VINICIUS RISPOLI'], classroom='S1', schedule='24M34', days=[
                'Segunda-Feira 10:00 às 11:50', 'Quarta-Feira 10:00 às 11:50'], _class="1", special_dates=[], discipline=self.discipline_2)
        self._class_3 = create_class(
            teachers=['RICARDO RAMOS FRAGELLI'], classroom='MOCAP', schedule='235M34',
            days=['Segunda-Feira 10:00 às 11:50', 'Terça-Feira 10:00 às 11:50', 'Quinta-Feira 10:00 às 11:50'], _class="1", special_dates=[], discipline=self.discipline_2)
        self._class_4 = create_class(
            teachers=['VINICIUS CARVALHO RISPOLI'], classroom='S1', schedule='35M34', days=[
                'Terça-Feira 10:00 às 11:50', 'Quinta-Feira 10:00 às 11:50'], _class="1", special_dates=[], discipline=self.discipline_2)
        self._class_5 = create_class(
            teachers=['RICARDO JUNIOR'], classroom='S1', schedule='35M34', days=[
                'Terça-Feira 10:00 às 11:50', 'Quinta-Feira 10:00 às 11:50'], _class="1", special_dates=[], discipline=self.discipline_1)
        self._class_6 = create_class(
            teachers=['LUIZA YOKO'], classroom='S1', schedule='35M34', days=[
                'Terça-Feira 10:00 às 11:50', 'Quinta-Feira 10:00 às 11:50'], _class="1", special_dates=[], discipline=self.discipline_3)

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

        response_1 = self.client.get(
            '/courses/?search=     &year=2023&period=2')
        response_2 = self.client.get(
            '/courses/?search=calculo&year=     &period=2')
        response_3 = self.client.get(
            '/courses/?search=calculo&year=2023&period=     ')
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

    def test_correct_search_with_teacher_full_name(self):
        """
        Testa a busca por disciplinas com nome completo de professor
        Testes:
        - Status code (200 OK)
        - Quantidade de disciplinas retornadas
        - Quantidade de turmas retornadas em cada disciplina
        - Código do departamento
        - Nome da disciplina
        - Professores da disciplina
        """
        response_for_disciplines = self.client.get(
            '/courses/?search=Ricardo Ramos Fragelli&year=2023&period=2')
        content = json.loads(response_for_disciplines.content)

        self.assertEqual(response_for_disciplines.status_code, 200)
        self.assertEqual(len(content), 1)

        # Testes da disciplina retornada
        self.assertEqual(content[0]['department']
                         ['code'], self.department.code)
        self.assertEqual(content[0]['name'], self.discipline_2.name)

        # Verifica a quantidade de turmas retornadas
        self.assertEqual(len(content[0]['classes']), 1)

        # Teste da 1ª turma do professor Ricardo
        self.assertEqual(content[0]['classes'][0]
                         ['teachers'], self._class_3.teachers)

    def test_correct_search_with_teacher_first_name_and_last_name(self):
        """
        Testa a busca por disciplinas com primeiro nome e sobrenome de professor
        Testes:
        - Status code (200 OK)
        - Quantidade de disciplinas retornadas
        - Quantidade de turmas retornadas em cada disciplina
        - Código do departamento
        - Nome da disciplina
        - Professores da disciplina
        """
        response_for_disciplines = self.client.get(
            '/courses/?search=Ricardo Fragelli&year=2023&period=2')
        content = json.loads(response_for_disciplines.content)

        # Teste da resposta da API
        self.assertEqual(response_for_disciplines.status_code, 200)
        self.assertEqual(len(content), 2)

        # Verifica a quantidade de turmas retornadas em cada disciplina
        self.assertEqual(len(content[0]['classes']), 1)
        self.assertEqual(len(content[1]['classes']), 1)

        # Testes da 1ª disciplina do professor Ricardo
        self.assertEqual(content[0]['department']
                         ['code'], self.department.code)
        self.assertEqual(content[0]['name'], self.discipline_1.name)
        self.assertEqual(content[0]['classes'][0]
                         ['teachers'], self._class_1.teachers)

        # Testes da 2ª disciplina do professor Ricardo
        self.assertEqual(content[1]['department']
                         ['code'], self.department.code)
        self.assertEqual(content[1]['name'], self.discipline_2.name)
        self.assertEqual(content[1]['classes'][0]
                         ['teachers'], self._class_3.teachers)

    def test_correct_search_with_teacher_first_name_with_one_discipline(self):
        """
        Testa a busca por disciplinas com primeiro nome de professor que leciona apenas uma disciplina
        Testes:
        - Status code (200 OK)
        - Quantidade de disciplinas retornadas
        - Quantidade de turmas retornadas em cada disciplina
        - Código do departamento
        - Nome da disciplina
        - Professores da disciplina
        """
        response_for_disciplines = self.client.get(
            '/courses/?search=vinicius&year=2023&period=2')
        content = json.loads(response_for_disciplines.content)

        # Teste da resposta da API
        self.assertEqual(response_for_disciplines.status_code, 200)
        self.assertEqual(len(content), 1)

        # Testes da disciplina retornada
        self.assertEqual(content[0]['department']
                         ['code'], self.department.code)
        self.assertEqual(content[0]['name'], self.discipline_2.name)

        # Verifica a quantidade de turmas retornadas
        self.assertEqual(len(content[0]['classes']), 2)

        # Teste da 1ª turma do professor Vinicius
        self.assertEqual(content[0]['classes'][0]
                         ['teachers'], self._class_2.teachers)

        # Teste da 2ª turma do professor Vinicius
        self.assertEqual(content[0]['classes'][1]
                         ['teachers'], self._class_4.teachers)

    def test_correct_search_with_teacher_first_name_with_more_than_one_discipline(self):
        """
        Testa a busca por disciplinas com primeiro nome de professor que leciona mais de uma disciplina
        Testes:
        - Status code (200 OK)
        - Quantidade de disciplinas retornadas
        - Quantidade de turmas retornadas em cada disciplina
        - Código do departamento
        - Nome da disciplina
        - Professores da disciplina
        """
        response_for_disciplines = self.client.get(
            '/courses/?search=ricardo&year=2023&period=2')
        content = json.loads(response_for_disciplines.content)

        # Testes da resposta da API
        self.assertEqual(response_for_disciplines.status_code, 200)
        self.assertEqual(len(content), 2)

        # Verifica a quantidade de turmas retornadas em cada disciplina
        self.assertEqual(len(content[0]['classes']), 2)
        self.assertEqual(len(content[1]['classes']), 1)

        # Testes da 1ª disciplina do professor Ricardo
        self.assertEqual(content[0]['department']
                         ['code'], self.department.code)
        self.assertEqual(content[0]['name'], self.discipline_1.name)
        self.assertEqual(content[0]['classes'][0]
                         ['teachers'], self._class_1.teachers)

        # Testes da 2ª disciplina do professor Ricardo
        self.assertEqual(content[1]['department']
                         ['code'], self.department.code)
        self.assertEqual(content[1]['name'], self.discipline_2.name)
        self.assertEqual(content[1]['classes'][0]
                         ['teachers'], self._class_3.teachers)

    def test_correct_search_with_teacher_last_name_with_one_discipline(self):
        """
        Testa a busca por disciplinas com sobrenome de professor que leciona apenas uma disciplina
        Testes:
        - Status code (200 OK)
        - Quantidade de disciplinas retornadas
        - Quantidade de turmas retornadas em cada disciplina
        - Código do departamento
        - Nome da disciplina
        - Professores da disciplina
        """
        response_for_disciplines = self.client.get(
            '/courses/?search=rispoli&year=2023&period=2')
        content = json.loads(response_for_disciplines.content)

        # Teste da resposta da API
        self.assertEqual(response_for_disciplines.status_code, 200)
        self.assertEqual(len(content), 1)

        # Testes da disciplina retornada
        self.assertEqual(content[0]['department']
                         ['code'], self.department.code)
        self.assertEqual(content[0]['name'], self.discipline_2.name)

        # Verifica a quantidade de turmas retornadas
        self.assertEqual(len(content[0]['classes']), 2)

        # Teste da 1ª turma do professor Vinicius
        self.assertEqual(content[0]['classes'][0]
                         ['teachers'], self._class_2.teachers)

        # Teste da 2ª turma do professor Vinicius
        self.assertEqual(content[0]['classes'][1]
                         ['teachers'], self._class_4.teachers)

    def test_correct_search_with_teacher_last_name_with_more_than_one_discipline(self):
        """
        Testa a busca por disciplinas com sobrenome de professor que leciona mais de uma disciplina
        Testes:
        - Status code (200 OK)
        - Quantidade de disciplinas retornadas
        - Quantidade de turmas retornadas em cada disciplina
        - Código do departamento
        - Nome da disciplina
        - Professores da disciplina
        """
        response_for_disciplines = self.client.get(
            '/courses/?search=fragelli&year=2023&period=2')
        content = json.loads(response_for_disciplines.content)

        # Testes da resposta da API
        self.assertEqual(response_for_disciplines.status_code, 200)
        self.assertEqual(len(content), 2)

        # Verifica a quantidade de turmas retornadas em cada disciplina
        self.assertEqual(len(content[0]['classes']), 1)
        self.assertEqual(len(content[1]['classes']), 1)

        # Testes da 1ª disciplina do professor Fragelli
        self.assertEqual(content[0]['department']
                         ['code'], self.department.code)
        self.assertEqual(content[0]['name'], self.discipline_1.name)
        self.assertEqual(content[0]['classes'][0]
                         ['teachers'], self._class_1.teachers)

        # Testes da 2ª disciplina do professor Fragelli
        self.assertEqual(content[1]['department']
                         ['code'], self.department.code)
        self.assertEqual(content[1]['name'], self.discipline_2.name)
        self.assertEqual(content[1]['classes'][0]
                         ['teachers'], self._class_3.teachers)

    def test_correct_search_with_class_schedule_and_department_code(self):
        """
        Testa a busca por disciplinas com horário de aula e código do departamento.
        É esperado que mais de uma disciplina seja retornada, pois o horário de aula é o mesmo para mais de uma disciplina.
        Testes:
        - Status code (200 OK)
        - Quantidade de disciplinas retornadas
        - Quantidade de turmas retornadas em cada disciplina
        - Código do departamento
        - Nome da disciplina
        - Professores da disciplina
        """
        schedule = '35M34'  # Horário das aulas
        department_code = '518'  # Código do departamento de matemática
        response_for_disciplines = self.client.get(
            f'/courses/?search=&year=2023&period=2&department_code={department_code}&schedule={schedule}')
        content = json.loads(response_for_disciplines.content)
        # Teste da resposta da API
        self.assertEqual(response_for_disciplines.status_code, 200)
        # As 3 disciplinas existentes no setUp devem ser retornadas
        self.assertEqual(len(content), 3)
        # Testes das disciplinas retornadas
        self.assertEqual(content[0]['department']
                         ['code'], self.department.code)
        # Testes da discipiina 1
        self.assertEqual(content[0]['name'], self.discipline_1.name)
        # Verifica a quantidade de turmas retornadas
        self.assertEqual(len(content[0]['classes']), 1)
        # Teste do professor da 1ª turma do horário 35M34
        self.assertEqual(content[0]['classes'][0]
                         ['teachers'], self._class_5.teachers)
        # Testes da 2ª disciplina retornada
        self.assertEqual(content[1]['department']
                         ['code'], self.department.code)
        # Verifica o nome da disciplina 2
        self.assertEqual(content[1]['name'], self.discipline_2.name)
        # Verifica a quantidade de turmas retornadas
        self.assertEqual(len(content[1]['classes']), 2)
        self.assertEqual(content[1]['classes'][0]
                         ['teachers'], self._class_3.teachers)
        self.assertEqual(content[1]['classes'][1]
                         ['teachers'], self._class_4.teachers)
        # Testes da 3ª disciplina retornada
        self.assertEqual(content[2]['department']
                         ['code'], self.department.code)
        # Verifica o nome da disciplina 3
        self.assertEqual(content[2]['name'], self.discipline_3.name)
        # Verifica a quantidade de turmas retornadas
        self.assertEqual(len(content[2]['classes']), 1)
        self.assertEqual(content[2]['classes'][0]
                         ['teachers'], self._class_6.teachers)

    def test_correct_search_with_class_name_and_schedule(self):
        """ Testa a busca por disciplinas com nome da matéria e horário de aula.
        Testes:
        - Status code (200 OK)
        - Quantidade de disciplinas retornadas
        - Quantidade de turmas retornadas em cada disciplina
        - Código do departamento
        - Nome da disciplina
        - Professores da disciplina
        """
        schedule = '35M34'
        name = 'calculo'
        response_for_disciplines = self.client.get(
            f'/courses/?search={name}&year=2023&period=2&schedule={schedule}')
        content = json.loads(response_for_disciplines.content)
        self.assertEqual(response_for_disciplines.status_code, 200)

        # Testa se retornou apenas as duas disciplinas de Cálculo presentes no setUp
        self.assertEqual(len(content), 2)
        self.assertEqual(content[0]['department']
                         ['code'], self.department.code)
        self.assertEqual(content[0]['name'], self.discipline_1.name)
        # Testa se para a disciplina 1 foi retornado apenas a turma com o schedule especificado.
        self.assertEqual(len(content[0]['classes']), 1)
        self.assertEqual(content[0]['classes'][0]
                         ['teachers'], self._class_5.teachers)

        self.assertEqual(content[1]['department']
                         ['code'], self.department.code)
        self.assertEqual(content[1]['name'], self.discipline_2.name)

        # Testa se para a disciplina 2 foi retornado as 2 turmas com o schedule especificado.
        self.assertEqual(len(content[1]['classes']), 2)
        self.assertEqual(content[1]['classes'][0]
                         ['teachers'], self._class_3.teachers)
        self.assertEqual(content[1]['classes'][1]
                         ['teachers'], self._class_4.teachers)

    def test_correct_search_with_class_name_and_schedule_but_no_classes_to_return(self):
        """
        Testa a busca por disciplinas com nome da matéria e horário de aula,
        mas não há turmas com o horário especificado.
        Testes:
        - Status code (200 OK)
        - Quantidade de disciplinas retornadas
        """
        schedule = '2N34'
        name = 'cálculo'
        response_for_disciplines = self.client.get(
            f'/courses/?search={name}&year=2023&period=2&schedule={schedule}')
        content = json.loads(response_for_disciplines.content)
        self.assertEqual(response_for_disciplines.status_code, 200)
        self.assertEqual(len(content), 0)
