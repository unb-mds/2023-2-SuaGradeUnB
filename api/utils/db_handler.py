from api.models import Discipline, Department, Class
from api.serializers import ClassSerializerSchedule
from api.models import Schedule
from api.decorators import handle_cache_before_delete

from users.models import User

from django.db.models.query import QuerySet
from django.contrib.postgres.search import SearchVector, SearchQuery, TrigramStrictWordSimilarity
from django.db.models.manager import BaseManager
from django.db.models import Q

import json

"""Este módulo lida com as operações de banco de dados."""


def get_or_create_department(code: str, name: str, year: str, period: str) -> Department:
    """Cria um departamento."""
    return Department.objects.get_or_create(code=code, name=name, year=year, period=period)[0]


def get_or_create_discipline(name: str, code: str, department: Department) -> Discipline:
    """Cria uma disciplina."""
    return Discipline.objects.get_or_create(name=name, code=code, department=department)[0]


def create_class(teachers: list, classroom: str, schedule: str,
                 days: list, _class: str, special_dates: list, discipline: Discipline) -> Class:
    """Cria uma turma de uma disciplina."""
    return Class.objects.create(teachers=teachers, classroom=classroom, schedule=schedule,
                                days=days, _class=_class, special_dates=special_dates, discipline=discipline)

@handle_cache_before_delete
def delete_classes_from_discipline(discipline: Discipline) -> QuerySet:
    """Deleta todas as turmas de uma disciplina."""
    return Class.objects.filter(discipline=discipline)


@handle_cache_before_delete
def delete_all_departments_using_year_and_period(year: str, period: str) -> QuerySet:
    """Deleta um departamento de um periodo especifico."""
    return Department.objects.filter(year=year, period=period)


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


def filter_disciplines_by_teacher(name: str) -> QuerySet:
    """Filtra as disciplinas pelo nome do professor na classe."""
    disciplines = Discipline.objects.all()
    search_words = name.split()

    query = Q()
    for word in search_words:
        query &= Q(classes__teachers__icontains=word)
    search_disciplines = disciplines.filter(query).distinct("id")

    return search_disciplines


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

    filtered_classes = classes.all()
    for special_date in kwargs.get("special_dates", []):
        filtered_classes = filtered_classes.filter(
            special_dates__contains=special_date
        )

    kwargs.pop("special_dates", None)
    try:
        return filtered_classes.get(**kwargs)
    except Class.DoesNotExist:
        return None


def save_schedule(user: User, schedule_to_save: list[Class]) -> bool:
    """Salva uma grade horária para um usuário."""

    serializer_data = ClassSerializerSchedule(schedule_to_save, many=True).data
    json_schedule = json.dumps(serializer_data)

    try:
        Schedule.objects.get_or_create(user=user, classes=json_schedule)
    except:  # pragma: no cover
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


def filter_classes_by_teacher(name: str, classes: QuerySet) -> QuerySet:
    """Filtra as turmas pelo nome do professor."""
    search_words = name.split()
    query = Q()

    for word in search_words:
        query &= Q(teachers__icontains=word)
    return classes.filter(query)
