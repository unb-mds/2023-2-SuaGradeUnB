from rest_framework.test import APITestCase
from utils import sessions as sns
from datetime import datetime

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

