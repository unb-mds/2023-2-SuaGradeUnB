from django.test import TestCase
from unittest.mock import Mock, patch
from utils.schedule_generator import ScheduleGenerator
from api.models import Class


class ScheduleGeneratorTestCase(TestCase):
    @patch('schedules.schedule_generator.get_class_by_id')
    def setUp(self, mock_get_class_by_id):
        self.mock_class1 = Mock(spec=Class)
        self.mock_class1.schedule = "MT123"
        self.mock_class1.discipline = "Math"
        self.mock_class1.id = "FGA0456"

        self.mock_class2 = Mock(spec=Class)
        self.mock_class2.schedule = "MT123"
        self.mock_class2.discipline = "Science"
        self.mock_class2.id = "FGA0123"

        mock_get_class_by_id.side_effect = [self.mock_class1, self.mock_class2]

        self.generator = ScheduleGenerator(
            classes_id=[self.mock_class1.id, self.mock_class2.id], preference=[1, 2, 3])

    def test_ct1_exception_class(self):
        # CT1: Teste de saída da matéria de exceção
        schedule = (self.mock_class1.id,)
        except_class = self.mock_class1
        result = self.generator._valid_schedule(schedule, except_class)
        self.assertTrue(result)

    def test_ct2_common_class(self):
        # CT2: Teste de saída de matéria comum
        schedule = (self.mock_class2.id,)
        result = self.generator._valid_schedule(schedule)
        self.assertTrue(result)

    def test_ct3_same_schedule(self):
        # CT3: Teste de matérias com o mesmo horário
        schedule = (self.mock_class1.id, self.mock_class2.id)
        except_class = None
        self.generator.schedule_info[self.mock_class1.schedule]["times"] = {
            ('M', 'T', '1', '2', '3')}
        self.generator.schedule_info[self.mock_class2.schedule]["times"] = {
            ('M', 'T', '1', '2', '3')}
        result = self.generator._valid_schedule(schedule, except_class)
        self.assertFalse(result)

    def test_ct4_same_schedule_except(self):
        # CT4: Teste de matérias com o mesmo horário, com uma classe de exceção
        schedule = (self.mock_class1.id, self.mock_class2.id)
        except_class = Mock(spec=Class)
        except_class.schedule = "XYZ123"
        self.generator.schedule_info[self.mock_class1.schedule]["times"] = {
            ('M', 'T', '1', '2', '3')}
        self.generator.schedule_info[self.mock_class2.schedule]["times"] = {
            ('M', 'T', '1', '2', '3')}
        result = self.generator._valid_schedule(schedule, except_class)
        self.assertFalse(result)
