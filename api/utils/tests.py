from string import ascii_letters as letters, digits
from collections import defaultdict
from rest_framework.test import APITestCase
from . import web_scraping as wbp, sessions as sns
from datetime import datetime
from django.urls import reverse
from pathlib import Path
import random
import json

from . import db_handler as dbh
from api.models import Department, Discipline, Class

class WebScrapingTest(APITestCase):

    def cookie(self):
        cookie = ""
        for _ in range(32):
            cookie += random.choice(letters + digits)

        return cookie

    def make_disciplines_request(self, path_name: str):
        current_path = Path(__file__).parent.absolute()
        infos_path = current_path / f"mock/infos.json"

        with open(infos_path) as json_file:
            data = json.load(json_file)

            year = data.get('year')
            period = data.get('period')
            department = data.get('department')

        url = reverse(f'utils:{path_name}')
        args = [department, year, period, url, self.client, self.cookie()]
        disciplines = wbp.get_department_disciplines(*args)

        return disciplines

    def test_get_list_of_departments(self):
        response = self.client.get(reverse('utils:sigaa'))

        departments = wbp.get_list_of_departments(response)
        self.assertEqual(type(list()), type(departments))
        if len(departments):
            self.assertEqual(type(str()), type(departments[0]))

    def test_get_list_of_departments_when_empty(self):
        response = self.client.get(reverse('utils:empty'))

        departments = wbp.get_list_of_departments(response)
        self.assertIsNone(departments)

    def test_get_department_disciplines(self):
        disciplines = self.make_disciplines_request('sigaa')

        self.assertEqual(type(disciplines), type(defaultdict(str)))
        if len(disciplines):
            keys = list(disciplines.keys())
            class_discipline = disciplines.get(keys[0])[0]

            self.assertTrue('name' in class_discipline)
            self.assertTrue('class_code' in class_discipline)
            self.assertTrue('teachers' in class_discipline)
            self.assertTrue('workload' in class_discipline)
            self.assertTrue('schedule' in class_discipline)
            self.assertTrue('days' in class_discipline)

    def test_get_department_disciplines_when_empty(self):
        disciplines = self.make_disciplines_request('empty')

        self.assertFalse(len(disciplines))

    def test_get_department_disciplines_when_without_tr_html_tag(self):
        disciplines = self.make_disciplines_request('table')

        self.assertFalse(len(disciplines))


class DateUtilsTest(APITestCase):

    def compare_date(self, date: datetime):
        before_dec = datetime(date.year, 12, 30) >= date
        after_may = datetime(date.year, 5, 1) <= date

        return before_dec and after_may

    def change_date(self, date: datetime):
        month = 2 if self.compare_date(date) else 6
        return datetime(date.year + self.compare_date(date), month=month, day=1)

    def test_get_current_year_and_period(self):
        year, period = sns.get_current_year_and_period()

        date = datetime.now()
        self.assertEqual(year, str(date.year))

        self.assertEqual((period == '2'), self.compare_date(date))
        self.assertEqual((period == '1'), not self.compare_date(date))

    def test_get_next_period(self):
        _, period = sns.get_next_period()

        date = datetime.now()
        self.assertEqual((period == '2'), not self.compare_date(date))
        self.assertEqual((period == '1'), self.compare_date(date))

        date = self.change_date(date)
        _, period = sns.get_next_period(date)

        self.assertEqual((period == '2'), not self.compare_date(date))
        self.assertEqual((period == '1'), self.compare_date(date))

    def test_get_next_period_with_year(self):
        year, period = sns.get_next_period()

        date = datetime.now()
        self.assertEqual(str(date.year + (not (period == '2'))), year)

        date = self.change_date(date)
        year, period = sns.get_next_period(date)

        self.assertEqual(str(date.year + (not (period == '2'))), year)

    def test_get_previous_period(self):
        _, period = sns.get_previous_period()

        date = datetime.now()
        self.assertEqual((period == '2'), not self.compare_date(date))
        self.assertEqual((period == '1'), self.compare_date(date))

        date = self.change_date(date)
        _, period = sns.get_previous_period(date)

        self.assertEqual((period == '2'), not self.compare_date(date))
        self.assertEqual((period == '1'), self.compare_date(date))

    def test_get_previous_period_with_year(self):
        year, period = sns.get_previous_period()

        date = datetime.now()
        self.assertEqual(str(date.year - (period == '2')), year)

        date = self.change_date(date)
        year, period = sns.get_previous_period(date)

        self.assertEqual(str(date.year - (period == '2')), year)

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
            workload = 60,
            teachers = ['Mateus Vieira'],
            classroom = 'Gather Town',
            schedule = '46M34',
            days = ['Quarta-Feira 10:00 às 11:50', 'Sexta-Feira 10:00 às 11:50'],
            _class = "1",
            discipline = discipline
        )

        self.assertEqual(_class.workload, 60)
        self.assertEqual(_class.teachers, ['Mateus Vieira'])
        self.assertEqual(_class.classroom, 'Gather Town')
        self.assertEqual(_class.schedule, '46M34')
        self.assertEqual(_class.days, ['Quarta-Feira 10:00 às 11:50', 'Sexta-Feira 10:00 às 11:50'])
        self.assertEqual(_class._class, "1")
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
            workload = 60,
            teachers = ['Henrique Camelo'],
            classroom = 'Gather Town',
            schedule = '46M34',
            days = ['Quarta-Feira 10:00 às 11:50', 'Sexta-Feira 10:00 às 11:50'],
            _class = "1",
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