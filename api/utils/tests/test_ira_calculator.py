from django.test import TestCase
from utils.ira_calculator import IraCalculator


class IraTestCase(TestCase):
    def setUp(self):
        self.ira_calc = IraCalculator()

    def test_one_discipline_with_MM(self):
        args = [
            {
                'mencao': 'MM',
                'semestre': 1,
                'qtdCreditos': 2,
            }
        ]

        self.assertEqual(self.ira_calc.get_ira_value(args), 3)

    def test_discipline_with_right_out_of_bounds_semester_value(self):
        args = [
            {
                'mencao': 'MM',
                'semestre': 7,
                'qtdCreditos': 2,
            },
        ]

        self.assertRaises(ValueError, self.ira_calc.get_ira_value, args)

    def test_discipline_with_left_out_of_bounds_semester_value(self):
        args = [
            {
                'mencao': 'MM',
                'semestre': 0,
                'qtdCreditos': 2,
            },
        ]

        self.assertRaises(ValueError, self.ira_calc.get_ira_value, args)


    def test_inexistent_grade(self):
        args = [
            {
                'mencao': 'NE',
                'semestre': 3,
                'qtdCreditos': 2,
            },
        ]
        self.assertRaises(ValueError, self.ira_calc.get_ira_value, args)

