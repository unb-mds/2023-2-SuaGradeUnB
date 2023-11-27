from django.db import models
from django.contrib.postgres.fields import ArrayField

class Department(models.Model):
    """Classe que representa um departamento.
    code:str -> Código do departamento
    year:str -> Ano do departamento
    period:str -> Período do departamento
    """
    code = models.CharField(max_length=10)
    year = models.CharField(max_length=4, default='0000')
    period = models.CharField(max_length=1, default='1')

    def __str__(self):
        return self.code

class Discipline(models.Model):
    """Classe que representa uma disciplina.
    name:str -> Nome da disciplina
    code:str -> Código da disciplina
    department:Department -> Departamento da disciplina
    """
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=64)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='disciplines')

    def __str__(self):
        return self.name

class Class(models.Model):
    """Classe que representa uma turma.
    teachers:list -> Lista de professores da turma
    classroom:str -> Sala da turma
    schedule:str -> Horário da turma
    days:list -> Dias da semana da turma
    _class:str -> Turma da disciplina
    discipline:Discipline -> Disciplina da turma
    """
    teachers = ArrayField(models.CharField(max_length=256))
    classroom = models.CharField(max_length=64)
    schedule = models.CharField(max_length=512)
    days = ArrayField(models.CharField(max_length=64))
    _class = models.CharField(max_length=64)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, related_name='classes')
    special_dates = ArrayField(
        ArrayField(
            models.CharField(max_length=256),
            size=3,
        ),
        default=list
    )

    def __str__(self):
        return self._class
