from rest_framework.test import APITestCase
from utils import db_handler as dbh
from utils.schedule_generator import ScheduleGenerator, LIMIT_ERROR_MESSAGE, PREFERENCE_RANGE_ERROR
from random import randint


class TestSchedule(APITestCase):
    def setUp(self):
        self.department = dbh.get_or_create_department(
            name='Instituto de Computação',
            code='CIC',
            year='2030',
            period='2'
        )
        self.discipline_1 = dbh.get_or_create_discipline(
            name='Programação Competitiva',
            code='CIC1234',
            department=self.department
        )
        self.class_1 = dbh.create_class(
            teachers=['Edson Alves'],
            classroom='I6',
            schedule='46T34',
            days=['Quarta-Feira 16:00 às 17:50', 'Sexta-Feira 16:00 às 17:50'],
            _class="1",
            special_dates=[],
            discipline=self.discipline_1
        )
        self.class_2 = dbh.create_class(
            teachers=['Edson Alves'],
            classroom='MOCAP',
            schedule='35T12',
            days=['Terça-Feira 14:00 às 15:50', 'Quinta-Feira 14:00 às 15:50'],
            _class="2",
            special_dates=[],
            discipline=self.discipline_1
        )
        self.class_3 = dbh.create_class(
            teachers=['VINICIUS RUELA'],
            classroom='PJC',
            schedule='24T45',
            days=['Segunda-Feira 16:00 às 17:50',
                  'Quarta-Feira 16:00 às 17:50'],
            _class="3",
            special_dates=[],
            discipline=self.discipline_1
        )
        self.class_4 = dbh.create_class(
            teachers=['VINICIUS RUELA'],
            classroom='PJC',
            schedule='35T12',
            days=['Terça-Feira 14:00 às 15:50', 'Quinta-Feira 14:00 às 15:50'],
            _class="4",
            special_dates=[],
            discipline=self.discipline_1
        )
        self.class_5 = dbh.create_class(
            teachers=["A definir"],
            classroom='A definir',
            schedule='7M1234',
            days=['Sábado 08:00 às 11:50'],
            _class="5",
            special_dates=[],
            discipline=self.discipline_1
        )
        self.discipline_2 = dbh.get_or_create_discipline(
            name='Estrutura de Dados',
            code='CIC1000',
            department=self.department
        )
        self.class_6 = dbh.create_class(
            teachers=['Fabiana'],
            classroom='MOCAP',
            schedule='35T12',
            days=['Terça-Feira 14:00 às 15:50', 'Quinta-Feira 14:00 às 15:50'],
            _class="1",
            special_dates=[],
            discipline=self.discipline_2
        )
        self.discipline_3 = dbh.get_or_create_discipline(
            name='CÁLCULO 2',
            code='MAT519',
            department=self.department
        )
        self.class_7 = dbh.create_class(
            teachers=['LUIZA YOKO'],
            classroom='S1',
            schedule='34T23',
            days=['Segunda-Feira 10:00 às 11:50',
                  'Quarta-Feira 10:00 às 11:50'],
            _class="1",
            special_dates=[],
            discipline=self.discipline_3
        )

    def test_with_correct_parameters(self):
        """
        Testa a geração de horários com todos os parâmetros corretos
        Os parâmetros enviados permitem que pelo menos uma solução seja encontrada
        """

        schedule_generator = ScheduleGenerator(classes_id=[
                                               self.class_1.id, self.class_2.id, self.class_3.id, self.class_4.id], preference=[3, 2, 1])
        generated_data = schedule_generator.generate()

        self.assertEqual(len(generated_data["schedules"]), 4)

    def test_with_higher_classes_limit(self):
        """
        Testa a geração de horários com um limite de classes maior que o número de classes permitidas para uma matéria
        """

        try:
            schedule_generator = ScheduleGenerator(classes_id=[
                                                   self.class_1.id, self.class_2.id, self.class_3.id, self.class_4.id, self.class_5.id], preference=[3, 2, 1])
        except Exception as error:
            self.assertEqual(str(error), LIMIT_ERROR_MESSAGE)

    def test_with_conflicting_classes(self):
        """
        Testa a geração de horários com classes conflitantes
        """

        schedule_generator = ScheduleGenerator(
            classes_id=[self.class_4.id, self.class_6.id, self.class_7.id])
        generated_data = schedule_generator.generate()

        self.assertFalse(len(generated_data["schedules"]))

    def test_with_empty_classes(self):
        """
        Testa a geração de horários com uma lista de classes vazia
        """

        schedule_generator = ScheduleGenerator(classes_id=[])
        generated_data = schedule_generator.generate()

        self.assertIsNone(generated_data)

    def test_with_invalid_class(self):
        """
        Testa a geração de horários com uma classe inválida
        """

        classes_ids = [self.class_1.id, self.class_2.id,
                       self.class_3.id, self.class_4.id]
        random_id = randint(1, 10000)

        while (random_id in classes_ids):  # pragma: no cover
            random_id = randint(1, 10000)

        try:
            schedule_generator = ScheduleGenerator(
                classes_id=classes_ids + [random_id])
        except Exception as error:
            self.assertEqual(
                str(error), f"class with id {random_id} does not exist.")

    def test_make_twice(self):
        """
        Testa a geração de horários duas vezes
        """

        schedule_generator = ScheduleGenerator(classes_id=[
                                               self.class_1.id, self.class_2.id, self.class_3.id, self.class_4.id], preference=[3, 2, 1])

        generated_data = schedule_generator.generate()
        schedules = generated_data["schedules"]
        self.assertEqual(len(schedules), 4)

        schedules = schedule_generator.generate()
        self.assertEqual(len(schedules), 4)

    def test_with_invalid_preference(self):
        """
        Testa a geração de horários com preferência inválida
        """

        try:
            schedule_generator = ScheduleGenerator(
                classes_id=[self.class_1.id], preference=[1, 2, '3'])
        except Exception as error:
            self.assertEqual(str(error), PREFERENCE_RANGE_ERROR)
