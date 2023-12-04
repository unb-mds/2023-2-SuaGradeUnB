from itertools import product
from collections import defaultdict
from .db_handler import get_class_by_id
from re import search
from api.models import Class


def check(function):
    """
    Decorator para verificar se a classe é válida antes de executar a função
    """

    def wrapper(self, *args, **kwargs):
        if not self.is_valid():
            return None
        return function(self, *args, **kwargs)

    return wrapper


class ScheduleGenerator:
    """Classe que representa um gerador de horários.
    Atributos:

    """

    def __init__(self, classes_id: list[int], preference: list = None):
        """Construtor da classe ScheduleGenerator
        """
        self.schedule_info = defaultdict(lambda: None)
        self.preference = preference
        self.generated = False
        self._get_and_validate_classes(classes_id=classes_id)
        self._make_disciplines_list()

    def _get_and_validate_classes(self, classes_id: list[int]) -> None:
        self.disciplines = defaultdict(list)
        self.classes = dict()
        self.schedules = []
        self.valid = True

        if not len(classes_id):
            self.valid = False
            return

        for class_id in classes_id:
            try:
                _class = get_class_by_id(id=class_id)

                self.classes[class_id] = _class
                self.disciplines[_class.discipline].append(class_id)
                self._add_schedule_code(_class.schedule)
            except Class.DoesNotExist:
                self.valid = False
                return

    def is_valid(self) -> bool:
        return self.valid

    # [3,2,1]
    def get_priority(self, days: list, turn: list[str], letter: str):
        """
        Calcula a prioridade de uma disciplina ser escolhida para a grade de horários.
        Quanto mais cedo for o horário, maior será a prioridade, independemente do turno.
        Quanto mais aulas na semana a disciplina tiver, maior será a prioridade.
        """
        letters = "MTN"
        turn_priority = 5 * (len(turn)) - sum(map(int, turn))
        days_quantity = len(days)

        priority = (self.preference[letters.find(
            letter)]) * (turn_priority + days_quantity)
        return priority

    def _add_schedule_code(self, schedules: str) -> None:
        if self.schedule_info[schedules] is not None:
            return

        regex = "[MTN]"
        schedules_list = schedules.split()
        schedules_dict = {
            "priority": 0,
            "times": set()
        }

        for schedule in schedules_list:
            match = search(regex, schedule)
            schedule = list(schedule)
            days = schedule[:match.start()]
            turn = schedule[match.start() + 1:]
            letter = match.group()

            values = [days, [letter], turn]
            code_product = product(*values)
            if self.preference is not None:
                schedules_dict["priority"] += self.get_priority(
                    days, turn, letter)

            schedules_dict["times"] = schedules_dict["times"].union(
                set(code_product))

        self.schedule_info[schedules] = schedules_dict

    @check
    def _make_disciplines_list(self) -> None:
        self.disciplines_list = []

        for classes in self.disciplines.values():
            self.disciplines_list.append(classes)

    def _is_valid_schedule(self, schedule: tuple) -> bool:
        codes_counter = 0
        schedule_codes = set()

        for class_id in schedule:
            _class = self.classes[class_id]
            schedule_code = self.schedule_info[_class.schedule]["times"]
            """Variável que contém o produto cartesiano dos horários"""
            codes_counter += len(schedule_code)
            """Contador do tamanho do conjunto de produtos cartesianos"""
            schedule_codes = schedule_codes.union(schedule_code)
            """Faz a união dos produtos cartesianos com o horário pretendido"""

            if codes_counter > len(schedule_codes):
                """Caso o contador seja maior do que a união dos produtos cartesianos com o horário pretendido,
                o horário não é válido, pois há horários que se sobrepõem"""
                return False

        return True

    def _add_schedule(self, schedule: tuple) -> None:
        parsed_schedule = []

        for class_id in schedule:
            _class = self.classes[class_id]
            parsed_schedule.append(_class)

        self.schedules.append(parsed_schedule)

    @check
    def generate(self) -> list | None:
        if self.generated:
            return self.schedules

        self.generated = True
        possible_schedules = product(*self.disciplines_list)

        for schedule in possible_schedules:
            if self._is_valid_schedule(schedule):
                print("valid", schedule)
                self._add_schedule(schedule)

        return self.sort_by_priority()

    def sort_by_priority(self):
        self.schedules.sort(key=lambda priority: sum(map(
            lambda _class: self.schedule_info[_class.schedule]["priority"], priority)), reverse=True)
        return self.schedules
