from api.models import Discipline, Department, Class

""" Este módulo lida com as operações de banco de dados."""


def get_or_create_department(code: str, year: str, period: str) -> Department:
    """Cria um departamento."""
    return Department.objects.get_or_create(code=code, year=year, period=period)[0]


def get_or_create_discipline(name: str, code: str, department: Department) -> Discipline:
    """Cria uma disciplina."""
    return Discipline.objects.get_or_create(name=name, code=code, department=department)[0]


def create_class(workload: int, teachers: list, classroom: str, schedule: str,
                 days: list, _class: str, discipline: Discipline) -> Class:
    """Cria uma turma de uma disciplina."""
    return Class.objects.create(workload=workload, teachers=teachers, classroom=classroom, schedule=schedule,
                                days=days, _class=_class, discipline=discipline)

def delete_classes_from_discipline(discipline: Discipline) -> None:
    """Deleta todas as turmas de uma disciplina."""
    Class.objects.filter(discipline=discipline).delete()

def delete_all_departments_using_year_and_period(year: str, period: str) -> None:
    """Deleta um departamento de um periodo especifico."""
    Department.objects.filter(year=year, period=period).delete()



