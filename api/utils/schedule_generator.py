from itertools import product
from collections import defaultdict, Counter
from .db_handler import get_class_by_id
from re import search
from api.models import Class

MAXIMUM_CLASSES_FOR_DISCIPLINE = 4
MINIMUM_PREFERENCE_RANGE = 1
MAXIMUM_PREFERENCE_RANGE = 3
MAXIMUM_DISCIPLINES = 11
MAXIMUM_DISPLAYED_CONFLICTS = 4

LIMIT_ERROR_MESSAGE = f"you can only send {MAXIMUM_DISCIPLINES} disciplines and {MAXIMUM_CLASSES_FOR_DISCIPLINE} classes for each discipline."
PREFERENCE_RANGE_ERROR = f"preference must be a list of integers with range [{MINIMUM_PREFERENCE_RANGE}, {MAXIMUM_PREFERENCE_RANGE}]"
NO_SCHEDULES_ERROR = "Não há horários disponíveis para a combinação de disciplinas selecionadas."
SUCCESS_MESSAGE = "Horários gerados com sucesso."
FIX_PROBLEM_MESSAGE = "\n\nPara resolver o problema, você pode remover uma das seguintes disciplinas: \n\n"

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
    """Classe que representa um gerador de horários."""
    available_letters = "MTN"

    def __init__(self, classes_id: list[int], preference: list = None):
        self.schedule_info = defaultdict(lambda: None)
        self.conflicting_classes = Counter()
        self.preference = preference
        self.generated = False
        self._validate_preference()
        self._get_and_validate_classes(classes_id=set(classes_id))
        self._make_disciplines_list()
        self._validate_parameters_length()

    def _validate_preference(self) -> None:
        self.valid = self.preference is None or all(isinstance(
            x, int) and MINIMUM_PREFERENCE_RANGE <= x <= MAXIMUM_PREFERENCE_RANGE for x in self.preference)

        if not self.valid:
            raise ValueError(PREFERENCE_RANGE_ERROR)

    @check
    def _get_and_validate_classes(self, classes_id: set[int]) -> None:
        self.disciplines = defaultdict(list)
        self.classes = dict()
        self.schedules = []

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
                raise ValueError(f"class with id {class_id} does not exist.")

    @check
    def _validate_parameters_length(self) -> None:
        if len(self.disciplines) > MAXIMUM_DISCIPLINES:  # pragma: no cover
            self.valid = False

        for classes in self.disciplines.values():
            if len(classes) > MAXIMUM_CLASSES_FOR_DISCIPLINE:
                self.valid = False
                break

        if not self.valid:
            raise ValueError(LIMIT_ERROR_MESSAGE)

    def is_valid(self) -> bool:
        return self.valid

    def _get_priority(self, days: list, turn: list[str], letter: str):
        """
        Calcula a prioridade de uma disciplina ser escolhida para a grade de horários.
        Quanto mais cedo for o horário, maior será a prioridade, independentemente do turno.
        Quanto mais aulas na semana a disciplina tiver, maior será a prioridade.
        """
        turn_priority = 5 * (len(turn)) - sum(map(int, turn))
        days_quantity = len(days)

        priority = self.preference[self.available_letters.find(
            letter)] * (turn_priority + days_quantity)

        return priority

    def _add_schedule_code(self, schedules: str) -> None:
        if self.schedule_info[schedules] is not None:
            return

        regex = f"[{self.available_letters}]"
        schedules_list = schedules.split()

        """Cria um dicionário com a prioridade e os horários
        em produto cartesiano de uma disciplina"""
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
                schedules_dict["priority"] += self._get_priority(
                    days, turn, letter)

            schedules_dict["times"] = schedules_dict["times"].union(
                set(code_product))

        self.schedule_info[schedules] = schedules_dict

    @check
    def _make_disciplines_list(self) -> None:
        self.disciplines_list = []

        for classes in self.disciplines.values():
            self.disciplines_list.append(classes)
            
    def _handle_conflict(self, conflicting_class: Class, schedule: tuple) -> None:
        # Depois, verificamos se há uma grade horária válida sem a disciplina atual
        schedule_valid = self._valid_schedule(schedule, conflicting_class)

        # Caso haja, adicionaremos a matéria removida na lista "conflicting_classes"
        if schedule_valid:
            self.conflicting_classes[conflicting_class.discipline] += 1

    def _valid_schedule(self, schedule: tuple, except_class: Class = None) -> bool:
        """
        Verifica se uma grade horária é válida. Caso não seja, verificamos se há a
        existência de uma grade horária após remoção de uma das disciplinas conflitantes.

        Caso haja, adicionaremos a matéria removida na lista "conflicting_classes" e,
        se não houver nenhuma grade horária válida, mostraremos para o usuário que
        ele pode escolher entre remover alguma das disciplinas conflitantes.

        :param schedule: Uma grade horária
        :param except_class: Uma disciplina em que não queremos verificar a existência de conflitos
        :return: True se a grade horária for válida, False caso contrário
        """

        time_from = dict()

        for class_id in schedule:
            _class = self.classes[class_id]
            schedule_code = self.schedule_info[_class.schedule]["times"]

            # Verificamos se a disciplina atual é a disciplina que queremos remover
            if _class == except_class:
                continue

            for code in schedule_code:
                if code not in time_from:
                    time_from[code] = _class
                    continue

                # Caso haja uma "except_class", significa que estamos na etapa de remoção de uma disciplina
                # conflitante. Portanto, não faremos nada.
                if except_class is not None:
                    return False

                conflicting_class = time_from[code]

                # Verificamos a ausência de conflito removendo a disciplina atual
                self._handle_conflict(_class, schedule)

                # Verificamos a ausência de conflito removendo a disciplina conflitante
                self._handle_conflict(conflicting_class, schedule)

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
            if self._valid_schedule(schedule):
                self._add_schedule(schedule)

        extra_message = SUCCESS_MESSAGE

        if not len(self.schedules):
            extra_message = NO_SCHEDULES_ERROR

        # Caso não haja nenhuma grade horária válida, mostraremos para o usuário que
        # ele pode escolher entre remover alguma das disciplinas conflitantes.
        if len(self.conflicting_classes):
            extra_message += FIX_PROBLEM_MESSAGE
            extra_message += "\n".join(map(
                lambda discipline: f"- {discipline[0].code}: {discipline[0].name}", self.conflicting_classes.most_common(MAXIMUM_DISPLAYED_CONFLICTS)))

        return {
            'message': extra_message,
            'schedules': self.sort_by_priority()
        }

    def sort_by_priority(self):
        self.schedules.sort(key=lambda priority: sum(map(
            lambda _class: self.schedule_info[_class.schedule]["priority"], priority)), reverse=True)

        return self.schedules
    
    def test_discipline_hour(self, discipline: str, hours: dict[str], departaments: dict[str], choice_disciplines: dict[str]):
        for key, values in departaments.items():
            for key_hours, values_hours in hours.items():
                for key_ch, values_ch in choice_disciplines.items():
                    if discipline == values and values == key_hours and values_hours == key_ch:
                            return values_ch 
                         
            
