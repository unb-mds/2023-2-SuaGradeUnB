from django.test import TestCase
from utils.ira_calculator import IraCalculator, Discipline


class IraTestCase(TestCase):
    def setUp(self):
        self.ira_calc = IraCalculator()

    def test_one_discipline_with_MM(self):
        args: list[Discipline] = [
            {
                'mencao': 'MM',
                'semestre': 1,
                'qtd_creditos': 2,
            }
        ]

        self.assertEqual(self.ira_calc.get_ira_value(args), 3)

    def test_discipline_with_right_out_of_bounds_semester_value(self):
        args: list[Discipline] = [
            {
                'mencao': 'MM',
                'semestre': 7,
                'qtd_creditos': 2,
            },
        ]

        self.assertRaises(ValueError, self.ira_calc.get_ira_value, args)

    def test_discipline_with_left_out_of_bounds_semester_value(self):
        args: list[Discipline] = [
            {
                'mencao': 'MM',
                'semestre': 0,
                'qtd_creditos': 2,
            },
        ]

        self.assertRaises(ValueError, self.ira_calc.get_ira_value, args)


    def test_inexistent_grade(self):
        args: list[Discipline] = [
            {
                'mencao': 'NE',
                'semestre': 3,
                'qtd_creditos': 2,
            },
        ]
        self.assertRaises(ValueError, self.ira_calc.get_ira_value, args)

    def test_multiple_disciplines_during_first_semester(self):
        args: list[Discipline] = [
            {
                'mencao': 'MM',
                'semestre': 1,
                'qtd_creditos': 4
            },
            {
                'mencao': 'MS',
                'semestre': 1,
                'qtd_creditos': 6
            },
            {
                'mencao': 'SS',
                'semestre': 1,
                'qtd_creditos': 6
            },
            {
                'mencao': 'SS',
                'semestre': 1,
                'qtd_creditos': 4
            },
            {
                'mencao': 'MS',
                'semestre': 1,
                'qtd_creditos': 4
            },
        ]

        self.assertEqual(self.ira_calc.get_ira_value(args), 4.25)



