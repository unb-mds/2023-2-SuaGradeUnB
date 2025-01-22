from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from ..views.save_schedule import SCHEDULES_LIMIT, SCHEDULES_LIMIT_ERROR_MSG, SCHEDULES_INVALID_SCHEDULES_MSG

from utils import db_handler as dbh

from api.serializers import ClassSerializerSchedule
from api.models import Class

from users.models import User

from api.tests.test_error_request_body_schedule_save import ErrorRequestBodyScheduleSave

import json


class TestScheduleSaveAPI(APITestCase, ErrorRequestBodyScheduleSave):

    def setDepartmentInfos(self):
        self.department_infos = [
            ('518', 'Departamento de Matemática e Estatística',
             '2023', '2'), ('673', 'Departamento de Matemática e Estatística', '2023', '2'),
            ('518', 'Departamento de Matemática e Estatística', '2024',
             '1'), ('673', 'Departamento de Matemática e Estatística', '2024', '1')
        ]

    def setDisciplineInfos(self):
        self.discipline_infos = [
            ('CÁLCULO 1', 'MAT0025',
             self.departments['department_0_2023_2']),
            ('CÁLCULO 1', 'MAT0025',
             self.departments['department_2_2024_1']),
            ('COMPILADORES 1', 'FGA0003',
             self.departments['department_1_2023_2']),
            ('COMPILADORES 1', 'FGA0003',
             self.departments['department_3_2024_1'])
        ]

    def setClassInfos(self):
        self.class_infos = [
            (['EDSON ALVES DA COSTA JUNIOR'], 'FGA - I8', '35T23',
             ['Terça-feira 14:00 às 15:50', 'Quinta-feira 14:00 às 15:50'],
             '1', [], self.disciplines['discipline_FGA0003_2023_2']),
            (['LUIS FILOMENO DE JESUS FERNANDES'], 'FGA - Sala I6', '46M34',
             ['Quarta-feira 10:00 às 11:50', 'Sexta-feira 10:00 às 11:50'],
             '2', [], self.disciplines['discipline_FGA0003_2023_2']),
            (['RICARDO RAMOS FRAGELLI'], 'FGA - I9', '246M34',
             ['Segunda-feira 10:00 às 11:50', 'Quarta-feira 10:00 às 11:50',
              'Sexta-feira 10:00 às 11:50'], '24', [],
             self.disciplines['discipline_MAT0025_2023_2']),
            (['EDSON ALVES DA COSTA JUNIOR'], 'FGA - I8', '24M34',
             ['Terça-feira 14:00 às 15:50', 'Quinta-feira 14:00 às 15:50'],
             '1', [], self.disciplines['discipline_FGA0003_2024_1']),
            (['LUIS FILOMENO DE JESUS FERNANDES'], 'FGA - Sala I6', '46M34',
             ['Quarta-feira 10:00 às 11:50', 'Sexta-feira 10:00 às 11:50'],
             '2', [], self.disciplines['discipline_FGA0003_2024_1']),
            (['RICARDO RAMOS FRAGELLI'], 'FGA - I9', '246M34',
             ['Segunda-feira 10:00 às 11:50', 'Quarta-feira 10:00 às 11:50',
              'Sexta-feira 10:00 às 11:50'], '24', [],
             self.disciplines['discipline_MAT0025_2024_1']),
            (['RICARDO RAMOS FRAGELLI'], 'FGA - I7', '24M34 5T23',
             ['Segunda-feira 10:00 às 11:50', 'Quarta-feira 10:00 às 11:50',
              'Quinta-feira 14:00 às 15:50'], '25', [],
             self.disciplines['discipline_MAT0025_2024_1']),
            (['RICARDO RAMOS FRAGELLI'], 'FGA - I7', '5T23',
             ['Quinta-feira 14:00 às 15:50'], '25', [['2024-01-01 - 2024-01-02', '1', '1']],
             self.disciplines['discipline_MAT0025_2024_1']),
            (['VINICIUS RISPOLI'], 'FGA - I9', '245M34',
             ['Segunda-feira 10:00 às 11:50', 'Quarta-feira 10:00 às 11:50',
              'Quinta-Feira 10:00 às 11:50'], '24', [],
             self.disciplines['discipline_MAT0025_2024_1']),
            (['MATEUS VIEIRA ROCHA'], 'FGA - I9', '236M34',
             ['Segunda-feira 10:00 às 11:50', 'Terça-feira 10:00 às 11:50',
              'Sexta-feira 10:00 às 11:50'], '24', [],
             self.disciplines['discipline_MAT0025_2024_1']),
            (['LUIZA YOKO'], 'FGA - I9', '346M34',
             ['Terça-feira 10:00 às 11:50', 'Quarta-feira 10:00 às 11:50',
              'Sexta-feira 10:00 às 11:50'], '24', [],
             self.disciplines['discipline_MAT0025_2024_1']),
            (['LUIZA YOKO'], 'FGA - I9', '456M34',
             ['Quarta-feira 10:00 às 11:50', 'Quinta-feira 10:00 às 11:50',
              'Sexta-feira 10:00 às 11:50'], '24', [],
             self.disciplines['discipline_MAT0025_2024_1']),

        ]

    def generate_schedule_structure(self, classes: list[Class]) -> list:
        schedule_structure = []

        for _class in classes:
            serializer_data = ClassSerializerSchedule(_class).data
            schedule_structure.append(serializer_data)

        return json.dumps(schedule_structure)

    def setUpDepartments(self):
        self.departments = {}
        self.setDepartmentInfos()
        for i, infos in enumerate(self.department_infos):
            code, name, year, period = infos
            new_department = dbh.get_or_create_department(
                code=code, name=name, year=year, period=period
            )
            self.departments[f'department_{i}_{year}_{period}'] = new_department

    def setUpDisciplines(self):
        self.disciplines = {}
        self.setDisciplineInfos()
        for name, code, department in self.discipline_infos:
            year, period = department.year, department.period
            new_discipline = dbh.get_or_create_discipline(
                name=name, code=code, department=department
            )
            self.disciplines[f'discipline_{code}_{year}_{period}'] = new_discipline

    def setUpClasses(self):
        self.classes = {}
        self.setClassInfos()
        for i, infos in enumerate(self.class_infos):
            teachers, classroom, schedule, days, _class, special_dates, discipline = infos
            year, period = discipline.department.year, discipline.department.period

            new_class = dbh.create_class(
                teachers=teachers, classroom=classroom, schedule=schedule,
                days=days, _class=_class, special_dates=special_dates,
                discipline=discipline
            )
            self.classes[f'class_{i}_{year}_{period}'] = new_class

    def setUp(self):
        self.setUpDepartments()
        self.setUpDisciplines()
        self.setUpClasses()

        self.user, _ = User.objects.get_or_create(
            first_name="test",
            last_name="banana",
            picture_url="https://photo.aqui.com",
            email="uiui@pichuruco.com",
        )
        self.user.save()

        tokens = TokenObtainPairSerializer.get_token(self.user)
        self.access_token = tokens.access_token

        self.url = reverse('api:schedules')
        self.content_type = 'application/json'

    def make_post_request(self, auth: str = 'correct_token', schedule: str = '[]'):
        headers = {'Authorization': f'Bearer {auth}1'}

        if auth == 'correct_token':
            headers = {'Authorization': f'Bearer {self.access_token}'}

        return self.client.post(
            self.url, schedule, headers=headers,
            content_type=self.content_type
        )

    def test_save_correct_schedule(self):
        """
        Testa o salvamento de uma grade horária correta com um usuário autenticado.

        Tests:
        - Classes salvas no banco de dados
        - Quantidade de classes salvas no banco de dados
        - Status code (201 CREATED)
        """
        schedule = self.generate_schedule_structure([
            self.classes['class_0_2023_2'],
            self.classes['class_2_2023_2']
        ])
        response = self.make_post_request(schedule=schedule)
        self.assertEqual(len(self.user.schedules.all()), 1)
        self.assertEqual(response.status_code, 201)

    def test_save_correct_schedule_with_special_dates(self):
        """
        Testa o salvamento de uma grade horária correta com um usuário autenticado.

        Tests:
        - Classes salvas no banco de dados
        - Quantidade de classes salvas no banco de dados
        - Status code (201 CREATED)
        """
        schedule = self.generate_schedule_structure([
            self.classes['class_3_2024_1'],
            self.classes['class_7_2024_1']
        ])

        response = self.make_post_request(schedule=schedule)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(self.user.schedules.all()), 1)

    def test_save_incorrect_schedule_with_different_year_period(self):
        """
        Testa o salvamento de uma grade horária com turmas de anos e períodos diferentes.

        Tests:
        - Mensagem de erro
        - Status code (400 BAD REQUEST)
        """
        schedule = self.generate_schedule_structure([
            self.classes['class_0_2023_2'],
            self.classes['class_5_2024_1']
        ])

        response = self.make_post_request(schedule=schedule)

        error_msg = 'all classes must have the same year and period'
        self.assertEqual(response.data.get('errors'), error_msg)
        self.assertEqual(response.status_code, 400)

    def test_save_incorrect_schedule_with_non_existing_class(self):
        """
        Testa o salvamento de uma grade horária com uma turma que não existe.

        Tests:
        - Mensagem de erro
        - Status code (400 BAD REQUEST)
        """
        schedule = self.generate_schedule_structure([
            self.classes['class_0_2023_2'],
            Class(
                teachers=['ADSON ALVES DA COSTA'], classroom='FGA - S10', schedule='35T23',
                days=['Terça-feira 14:00 às 15:50', 'Quinta-feira 14:00 às 15:50'], _class='1',
                special_dates=[], discipline=self.disciplines['discipline_FGA0003_2023_2']
            )
        ])

        response = self.make_post_request(schedule=schedule)

        error_msg = 'the class FGA0003 does not exists with this params'
        self.assertEqual(response.data.get('errors'), error_msg)
        self.assertEqual(response.status_code, 400)

    def test_save_incorrect_schedule_with_compatible_classes(self):
        """
        Testa o salvamento de uma grade horária com turmas que não são compatíveis.

        Tests:
        - Mensagem de erro
        - Status code (400 BAD REQUEST)
        """
        schedule = self.generate_schedule_structure([
            self.classes['class_3_2024_1'],
            self.classes['class_6_2024_1']
        ])

        response = self.make_post_request(schedule=schedule)

        error_msg = SCHEDULES_INVALID_SCHEDULES_MSG
        self.assertEqual(response.data.get('errors'), error_msg)
        self.assertEqual(response.status_code, 400)

    def test_save_correct_schedule_without_auth(self):
        """
        Testa o salvamento de uma grade horária sem um usuário autenticado.

        Tests:
        - Status code (403 FORBIDDEN)
        """
        schedule = self.generate_schedule_structure([
            self.classes['class_0_2023_2'],
            self.classes['class_2_2023_2']
        ])

        response = self.make_post_request(auth=False, schedule=schedule)

        self.assertEqual(response.status_code, 403)

    def test_save_correct_schedule_with_incorrect_auth_token(self):
        """
        Testa o salvamento de uma grade horária com um token de autenticação incorreto.

        Tests:
        - Status code (403 FORBIDDEN)
        """
        schedule = self.generate_schedule_structure([
            self.classes['class_0_2023_2'],
            self.classes['class_2_2023_2']
        ])

        token = 'incorrect_token'
        response = self.make_post_request(auth=token, schedule=schedule)

        self.assertEqual(response.status_code, 403)

    def test_save_limit_reached(self):
        """
        Testa o salvamento de uma grade horária quando o limite de grades horárias é atingido.
        Salva todas as grades horárias possíveis e tenta salvar mais uma.

        Tests:
        - Status code (400 BAD REQUEST)
        """

        for i in range(3):
            schedule = self.generate_schedule_structure([
                self.classes[f'class_{i}_2023_2']
            ])

            response = self.make_post_request(schedule=schedule)
            self.assertEqual(response.status_code, 201)

        for i in range(3, SCHEDULES_LIMIT):
            schedule = self.generate_schedule_structure([
                self.classes[f'class_{i}_2024_1']
            ])
            response = self.make_post_request(schedule=schedule)
            self.assertEqual(response.status_code, 201)

        schedule = self.generate_schedule_structure([
            self.classes[f'class_{SCHEDULES_LIMIT-1}_2024_1']
        ])

        response = self.make_post_request(schedule=schedule)
        self.assertEqual(response.data.get('errors'),
                         SCHEDULES_LIMIT_ERROR_MSG)
        self.assertEqual(response.status_code, 400)
