from django.test import TestCase
from .models import Department, Discipline

class DisciplineTests(TestCase):
    def setUp(self):
        self.department = Department.objects.create(
            name = 'Departamento de Informática',
            code = 'INF',
        )

        self.discipline = Discipline.objects.create(
            name = 'Métodos de Desenvolvimento de Software',
            code = 'MDS1010',
            workload = 60,
            teachers = ['Professor 1', 'Professor 2'],
            classroom = 'MOCAP',
            schedule = '46M34',
            days = ['Quarta-Feira 10:00 às 11:50', 'Sexta-Feira 10:00 às 11:50'],
            _class = 1,
            department = self.department
        )

    
    def test_create_discipline(self):
        self.assertEqual(self.discipline.name, 'Métodos de Desenvolvimento de Software')
        self.assertEqual(self.discipline.code, 'MDS1010')
        self.assertEqual(self.discipline.workload, 60)
        self.assertEqual(self.discipline.teachers, ['Professor 1', 'Professor 2'])
        self.assertEqual(self.discipline.classroom, 'MOCAP')
        self.assertEqual(self.discipline.schedule, '46M34')
        self.assertEqual(self.discipline.days, ['Quarta-Feira 10:00 às 11:50', 'Sexta-Feira 10:00 às 11:50'])
        self.assertEqual(self.discipline._class, 1)
        self.assertEqual(self.discipline.department, self.department)
    
    def test_create_department(self):
        self.assertEqual(self.department.name, 'Departamento de Informática')
        self.assertEqual(self.department.code, 'INF')
