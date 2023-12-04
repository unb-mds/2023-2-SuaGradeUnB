from itertools import product
from collections import defaultdict
from .db_handler import get_class_by_id
from re import search
from api.models import Class

def check(function):
    def wrapper(self, *args, **kwargs):
        if not self.is_valid():
            return None
        return function(self, *args, **kwargs)
    
    return wrapper

class ScheduleGenerator:    
    def __init__(self, classes_id: list[int], preference: [] = [1, 1, 1]):
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
            
            # schedules_dict["priority"] += _get_priority(letter)
            schedules_dict["times"] = schedules_dict["times"].union(set(code_product))
        
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
            codes_counter += len(schedule_code)
            schedule_codes = schedule_codes.union(schedule_code)
                        
            if codes_counter > len(schedule_codes):
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
        
        return self.schedules