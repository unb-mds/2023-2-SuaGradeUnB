from itertools import product
from collections import defaultdict, Counter
from ..db_handler import get_class_by_id
from re import search
from api.models import Class
from schedule_generator import discipline_hour

class Test_discipline:
    """Esse Teste ainda não passa, pois é necessário passar parametros dentro dos dicionarios na função principal"""
    def test_discipline_hour(self):
        self.AssertEqual(discipline_hour("MD2", {"10:45":"MD2", "11:00":"FSO"}, {"Matematica":"10:45", "Sistemas Operacionais": "11:00"}, {"MD2":"Matematica Discreta 2", "FSO":"Fundamentos de Sistemas Operacionais"}, "Matematica Discreta 2")) 