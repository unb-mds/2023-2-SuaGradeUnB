from django.test import TestCase
from .models import Department, Discipline,Class

class DisciplineModelsTest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(
            code = 'INF',
            year = "2023",
            period = "2"
        )

        self.discipline = Discipline.objects.create(
            name = 'Métodos de Desenvolvimento de Software',
            code = 'MDS1010',
            department = self.department
        )
        self._class = Class.objects.create(
            workload = 60,
            teachers = ['Professor 1', 'Professor 2'],
            classroom = 'MOCAP',
            schedule = '46M34',
            days = ['Quarta-Feira 10:00 às 11:50', 'Sexta-Feira 10:00 às 11:50'],
            _class = "1",
            discipline = self.discipline
        )


    def test_create_discipline(self):
        self.assertEqual(self.discipline.name, 'Métodos de Desenvolvimento de Software')
        self.assertEqual(self.discipline.code, 'MDS1010')
        self.assertEqual(self.discipline.department, self.department)

    def test_create_class(self):
        self.assertEqual(self._class.workload, 60)
        self.assertEqual(self._class.teachers, ['Professor 1', 'Professor 2'])
        self.assertEqual(self._class.classroom, 'MOCAP')
        self.assertEqual(self._class.schedule, '46M34')
        self.assertEqual(self._class.days, ['Quarta-Feira 10:00 às 11:50', 'Sexta-Feira 10:00 às 11:50'])
        self.assertEqual(self._class._class, "1")
        self.assertEqual(self._class.discipline, self.discipline)

    def test_create_department(self):
        self.assertEqual(self.department.code, 'INF')
        self.assertEqual(self.department.year, '2023')
        self.assertEqual(self.department.period, '2')
