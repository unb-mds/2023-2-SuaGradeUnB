from api.models import Discipline, Department, Class
from django.db.models.query import QuerySet
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramStrictWordSimilarity
from django.db.models import Q
""" Este módulo lida com as operações de banco de dados."""


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

def filter_disciplines_by_name(name: str, disciplines: Discipline = Discipline.objects) -> QuerySet:
    """Filtra as disciplinas pelo nome."""
    return disciplines.filter(name__unaccent__icontains=name)

def get_best_similarities_by_name(name: str, disciplines: Discipline = Discipline.objects, config="portuguese_unaccent") -> QuerySet:
    """Filtra as disciplinas pelo nome."""
    vector = SearchVector("name", config=config)
    query = SearchQuery(name, config=config)
    rank = SearchRank(vector, query)
    values = disciplines.annotate(
        search=vector,
        rank=rank,
        similarity=TrigramStrictWordSimilarity(name, "name")
    ).filter(
        Q(search=query) | Q(similarity__gt=0.2)
    ).all().order_by("-similarity")

    return values

def filter_disciplines_by_code(code: str, disciplines: Discipline = Discipline.objects) -> QuerySet:
    """Filtra as disciplinas pelo código."""
    return disciplines.filter(code__icontains=code)

def filter_disciplines_by_year_and_period(year: str, period: str, disciplines: Discipline = Discipline.objects) -> QuerySet:
    """Filtra as disciplinas pelo ano e período."""
    return disciplines.filter(department__year=year, department__period=period)

