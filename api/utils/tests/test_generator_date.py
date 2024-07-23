from rest_framework.test import APITestCase
from utils import sessions as sns
from datetime import datetime

class TestGeneratorDate(APITestCase):

    def test_valid_generator_date(self):
        # Testando datas válidas que devem retornar período "1"
        list_dates = [
            datetime(2024, 1, 1),
            datetime(2024, 2, 1),
            datetime(2024, 3, 1),
            datetime(2024, 4, 1)
        ]
        
        for date in list_dates:
            year, period = sns.get_current_year_and_period(date)
            self.assertEqual("2024", year)
            self.assertEqual("1", period)
    
    def test_valid_generator_date_period_2(self):
        # Testando datas válidas que devem retornar período "2"
        list_dates_period_2 = [
            datetime(2024, 5, 2),
            datetime(2024, 6, 1),
            datetime(2024, 10, 1),
            datetime(2024, 12, 31),
            datetime(2025, 1, 1)
        ]
        
        for date in list_dates_period_2:
            year, period = sns.get_current_year_and_period(date)
            self.assertEqual("2024", year)
            self.assertEqual("2", period)

    def test_generator_date_none(self):
        # Testando o caso onde a data é None
        year, period = sns.get_current_year_and_period(None)
        expected_year = str(datetime.now().year)
        if datetime.now() >= datetime(datetime.now().year, 5, 2):
            expected_period = "2"
        else:
            expected_period = "1"
        self.assertEqual(expected_year, year)
        self.assertEqual(expected_period, period)
    
    def test_invalid_generator_date(self):
        # Testando datas que não devem estar no período "2"
        list_dates_invalid = [
            datetime(2024, 5, 1),
            datetime(2025, 1, 2),
            datetime(2024, 4, 30)
        ]
        
        for date in list_dates_invalid:
            year, period = sns.get_current_year_and_period(date)
            if date.year == 2025:
                self.assertEqual("2025", year)
            else:
                self.assertEqual("2024", year)
            self.assertEqual("1", period)     
       
           
