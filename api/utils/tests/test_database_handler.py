from rest_framework.test import APITestCase
from utils import db_handler as dbh
from api.models import Department

class DatabaseHandlerTest(APITestCase):
    def test_create_department(self):
        department = dbh.get_or_create_department(
            code = 'TCC',
            year = '2025',
            period = '1'
        )

        self.assertEqual(department.code, 'TCC')
        self.assertEqual(department.year, '2025')
        self.assertEqual(department.period, '1')

    def test_create_discipline(self):
        department = dbh.get_or_create_department(
            code = 'SGU',
            year = '2023',
            period = '2'
        )

        discipline = dbh.get_or_create_discipline(
            name = 'Front-End II',
            code = 'SGU1234',
            department = department
        )

        self.assertEqual(discipline.name, 'Front-End II')
        self.assertEqual(discipline.code, 'SGU1234')
        self.assertTrue(discipline.department == department)
    
    def test_create_class(self):
        department = dbh.get_or_create_department(
            code = 'SGU',
            year = '2023',
            period = '2'
        )

        discipline = dbh.get_or_create_discipline(
            name = 'Front-End II',
            code = 'SGU1234',
            department = department
        )

        _class = dbh.create_class(
            teachers = ['Mateus Vieira'],
            classroom = 'Gather Town',
            schedule = '46M34',
            days = ['Quarta-Feira 10:00 às 11:50', 'Sexta-Feira 10:00 às 11:50'],
            _class = "1",
            special_dates=[],
            discipline = discipline
        )

        self.assertEqual(_class.teachers, ['Mateus Vieira'])
        self.assertEqual(_class.classroom, 'Gather Town')
        self.assertEqual(_class.schedule, '46M34')
        self.assertEqual(_class.days, ['Quarta-Feira 10:00 às 11:50', 'Sexta-Feira 10:00 às 11:50'])
        self.assertEqual(_class._class, "1")
        self.assertEqual(_class.special_dates, [])
        self.assertTrue(_class.discipline == discipline)
        
    def test_delete_classes_from_discipline(self):
        department = dbh.get_or_create_department(
            code = 'HCQ',
            year = '2023',
            period = '2'
        )

        discipline = dbh.get_or_create_discipline(
            name = 'Lingua Portuguesa (Portugal)',
            code = 'HCQ1234',
            department = department
        )

        _class = dbh.create_class(
            teachers = ['Henrique Camelo'],
            classroom = 'Gather Town',
            schedule = '46M34',
            days = ['Quarta-Feira 10:00 às 11:50', 'Sexta-Feira 10:00 às 11:50'],
            _class = "1",
            special_dates=['20/12/2023 - 30/12/2023'],
            discipline = discipline
        )

        dbh.delete_classes_from_discipline(
            discipline = discipline
        )

        self.assertFalse(len(discipline.classes.all()))
    
    def test_delete_all_departments_using_year_and_period(self):
        department = dbh.get_or_create_department(
            code = 'MDS',
            year = '2025',
            period = '2'
        )

        dbh.delete_all_departments_using_year_and_period(
            year = '2025',
            period = '2'
        )

        self.assertFalse(len(Department.objects.all()))
    
    def test_filter_disciplines_by_name(self):
        department = dbh.get_or_create_department(
            code = 'CFH',
            year = '2023',
            period = '2'
        )

        discipline = dbh.get_or_create_discipline(
            name = 'Aprendizado de organização de faltas',
            code = 'CFH1234',
            department = department
        )

        disciplines = dbh.filter_disciplines_by_name(
            name = 'Aprendizado de organização de faltas'
        )

        self.assertTrue(len(disciplines))
        self.assertTrue(discipline in disciplines)
    
    def test_filter_disciplines_by_code(self):
        department = dbh.get_or_create_department(
            code = 'FGA',
            year = '2023',
            period = '2'
        )

        discipline = dbh.get_or_create_discipline(
            name = 'Tópicos Especiais em Programação',
            code = 'FGA0053',
            department = department
        )

        disciplines = dbh.filter_disciplines_by_code(
            code = 'FGA0053'
        )

        self.assertTrue(len(disciplines))
        self.assertTrue(discipline in disciplines)
    
    def test_filter_disciplines_by_year_and_period(self):
        department = dbh.get_or_create_department(
            code = 'THZ',
            year = '2027',
            period = '1'
        )

        discipline = dbh.get_or_create_discipline(
            name = 'Redes',
            code = 'THZ1004',
            department = department
        )

        disciplines = dbh.filter_disciplines_by_year_and_period(
            year = '2027',
            period = '1'
        )

        self.assertTrue(len(disciplines))
        self.assertTrue(discipline in disciplines)
