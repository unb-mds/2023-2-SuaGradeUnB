from django.test import TestCase
from django.core.cache import cache
from api.models import Department, Discipline, Class


class ModelsTest(TestCase):
    def create_data(self):
        self.department = Department.objects.create(
            name='Instituto de Informática',
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
            teachers=['Professor 1', 'Professor 2'],
            classroom='MOCAP',
            schedule='46M34',
            days=['Quarta-Feira 10:00 às 11:50', 'Sexta-Feira 10:00 às 11:50'],
            _class="1",
            discipline=self.discipline
        )

        cache.set("INF/2023.2", "hash_value")

    def setUp(self):
        self.create_data()

    def test_create_discipline(self):
        self.assertEqual(self.discipline.name,
                         'Métodos de Desenvolvimento de Software')
        self.assertEqual(self.discipline.code, 'MDS1010')
        self.assertEqual(self.discipline.department, self.department)

    def test_create_class(self):
        self.assertEqual(self._class.teachers, ['Professor 1', 'Professor 2'])
        self.assertEqual(self._class.classroom, 'MOCAP')
        self.assertEqual(self._class.schedule, '46M34')
        self.assertEqual(self._class.days, [
                         'Quarta-Feira 10:00 às 11:50', 'Sexta-Feira 10:00 às 11:50'])
        self.assertEqual(self._class._class, "1")
        self.assertEqual(self._class.discipline, self.discipline)

    def test_create_department(self):
        self.assertEqual(self.department.name, 'Instituto de Informática')
        self.assertEqual(self.department.code, 'INF')
        self.assertEqual(self.department.year, '2023')
        self.assertEqual(self.department.period, '2')

    def test_str_method_of_discipline(self):
        self.assertEqual(str(self.discipline), self.discipline.name)

    def test_str_method_of_class(self):
        self.assertEqual(str(self._class), self._class._class)

    def test_str_method_of_department(self):
        self.assertEqual(str(self.department), self.department.code)

    def test_delete_department_with_cache_handle(self):
        self.department.delete()

        empty_model = not len(Department.objects.all())
        empty_cache = not len(cache.keys('*'))

        self.assertTrue(empty_model)
        self.assertTrue(empty_cache)

    def test_delete_discipline_with_cache_handle(self):
        self.discipline.delete()

        empty_model = not len(Discipline.objects.all())
        empty_cache = not len(cache.keys('*'))

        self.assertTrue(empty_model)
        self.assertTrue(empty_cache)

    def test_delete_class_with_cache_handle(self):
        self._class.delete()

        empty_model = not len(Class.objects.all())
        empty_cache = not len(cache.keys('*'))

        self.assertTrue(empty_model)
        self.assertTrue(empty_cache)
