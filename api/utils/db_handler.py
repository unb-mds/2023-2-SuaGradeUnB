from api.models import Discipline, Department, Class
from api.serializers import ClassSerializerSchedule
from api.models import Schedule

from users.models import User

from django.db.models.query import QuerySet
from django.contrib.postgres.search import SearchVector, SearchQuery, TrigramStrictWordSimilarity
from django.db.models.manager import BaseManager
from django.db.models import Q

import json

"""Este módulo lida com as operações de banco de dados."""


def get_or_create_department(code: str, year: str, period: str) -> Department:
    """Cria um departamento."""
    return Department.objects.get_or_create(code=code, year=year, period=period)[0]


def get_or_create_discipline(name: str, code: str, department: Department) -> Discipline:
    """Cria uma disciplina."""
    return Discipline.objects.get_or_create(name=name, code=code, department=department)[0]


def create_class(teachers: list, classroom: str, schedule: str,
                 days: list, _class: str, special_dates: list, discipline: Discipline) -> Class:
    """Cria uma turma de uma disciplina."""
    return Class.objects.create(teachers=teachers, classroom=classroom, schedule=schedule,
                                days=days, _class=_class, special_dates=special_dates, discipline=discipline)


def delete_classes_from_discipline(discipline: Discipline) -> None:
    """Deleta todas as turmas de uma disciplina."""
    Class.objects.filter(discipline=discipline).delete()


def delete_all_departments_using_year_and_period(year: str, period: str) -> None:
    """Deleta um departamento de um periodo especifico."""
    Department.objects.filter(year=year, period=period).delete()


def get_best_similarities_by_name(name: str, disciplines: Discipline = Discipline.objects, config="portuguese_unaccent") -> QuerySet:
    """Filtra as disciplinas pelo nome."""
    vector = SearchVector("unicode_name", config=config)
    query = SearchQuery(name, config=config)
    values = disciplines.annotate(
        search=vector,
        similarity=TrigramStrictWordSimilarity(name, "unicode_name")
    ).filter(
        Q(search=query) | Q(similarity__gt=0)
    ).all().order_by("-similarity")

    return values


def filter_disciplines_by_code(code: str, disciplines: Discipline = Discipline.objects) -> QuerySet:
    """Filtra as disciplinas pelo código."""
    return disciplines.filter(code__icontains=code)


def filter_disciplines_by_year_and_period(year: str, period: str, disciplines: Discipline = Discipline.objects) -> QuerySet:
    """Filtra as disciplinas pelo ano e período."""
    return disciplines.filter(department__year=year, department__period=period)


def get_class_by_id(id: int, classes: BaseManager[Class] = Class.objects) -> Class:
    """Filtra as turmas pelo id."""
    return classes.get(id=id)


def get_class_by_params(classes: BaseManager[Class] = Class.objects, **kwargs) -> Class | None:
    """Filtra as turmas pelos argumentos: nome, código, departamento, ..."""
    try:
        return classes.get(**kwargs)
    except Class.DoesNotExist:
        return None


def save_schedule(user: User, schedule_to_save: list[Class]) -> bool:
    """Salva uma grade horária para um usuário."""

    serializer_data = ClassSerializerSchedule(schedule_to_save, many=True).data
    json_schedule = json.dumps(serializer_data)

    try:
        Schedule.objects.get_or_create(user=user, classes=json_schedule)
    except: # pragma: no cover
        return False

    return True

def get_schedules(user: User) -> QuerySet:
    """Retorna as grades horárias de um usuário."""
    return Schedule.objects.filter(user=user).all()

def delete_schedule(user: User, id: int) -> bool:
    """Deleta uma grade horária de um usuário."""
    try:
        Schedule.objects.get(user=user, id=id).delete()
    except Schedule.DoesNotExist:
        return False

    return True
