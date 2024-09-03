from django.test import TestCase
from utils.ira_calculator import IraCalculator, Discipline


class IraTestCase(TestCase):
    def setUp(self):
        self.ira_calc = IraCalculator()

    def test_one_discipline_with_MM(self):
        args: list[Discipline] = [
            {
                'grade': 'MM',
                'semester': 1,
                'number_of_credits': 2,
            }
        ]

        self.assertEqual(self.ira_calc.get_ira_value(args), 3)

    def test_discipline_with_left_out_of_bounds_semester_value(self):
        args: list[Discipline] = [
            {
                'grade': 'MM',
                'semester': 0,
                'number_of_credits': 2,
            },
        ]

        self.assertRaises(ValueError, self.ira_calc.get_ira_value, args)

    def test_discipline_with_incorrect_semester_type(self):
        args: list[Discipline] = [
            {
                'grade': 'MM',
                'semester': '0',
                'number_of_credits': 2,
            },
        ]

        self.assertRaises(TypeError, self.ira_calc.get_ira_value, args)


    def test_inexistent_grade(self):
        args: list[Discipline] = [
            {
                'grade': 'NE',
                'semester': 3,
                'number_of_credits': 2,
            },
        ]
        self.assertRaises(ValueError, self.ira_calc.get_ira_value, args)

    def test_multiple_disciplines_during_first_semester(self):
        args: list[Discipline] = [
            {
                'grade': 'MM',
                'semester': 1,
                'number_of_credits': 4
            },
            {
                'grade': 'MS',
                'semester': 1,
                'number_of_credits': 6
            },
            {
                'grade': 'SS',
                'semester': 1,
                'number_of_credits': 6
            },
            {
                'grade': 'SS',
                'semester': 1,
                'number_of_credits': 4
            },
            {
                'grade': 'MS',
                'semester': 1,
                'number_of_credits': 4
            },
        ]

        self.assertEqual(self.ira_calc.get_ira_value(args), 4.25)

    def test_negative_number_of_credits(self):
        args: list[Discipline] = [
            {
                'grade': 'MM',
                'semester': 3,
                'number_of_credits': -1,
            },
        ]
        self.assertRaises(ValueError, self.ira_calc.get_ira_value, args)

    def test_null_number_of_credits(self):
        args: list[Discipline] = [
            {
                'grade': 'MM',
                'semester': 3,
                'number_of_credits': -1,
            },
        ]
        self.assertRaises(ValueError, self.ira_calc.get_ira_value, args)

    def test_none_number_of_credits(self):
        args: list[Discipline] = [
            {
                'grade': 'MM',
                'semester': 2,
                'number_of_credits': None,
            },
        ]
        self.assertRaises(TypeError, self.ira_calc.get_ira_value, args)

    def tests_discipline_with_lowercase_grade_value(self):
        args: list[Discipline] = [
            {
                'grade': 'mm',
                'semester': 1,
                'number_of_credits': 2,
            }
        ]

        self.assertEqual(self.ira_calc.get_ira_value(args), 3)
