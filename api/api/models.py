from django.db import models
from django.contrib.postgres.fields import ArrayField

class Department(models.Model):
    # Classe que representa um departamento
    code = models.CharField(max_length=10, unique=True)
    year = models.CharField(max_length=4, default='0000')
    period = models.CharField(max_length=1, default='1')

    def __str__(self):
        return self.code

class Discipline(models.Model):
    # Classe que representa uma disciplina
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='disciplines')

    def __str__(self):
        return self.name

class Class(models.Model):
    workload = models.IntegerField()
    teachers = ArrayField(models.CharField(max_length=50))
    classroom = models.CharField(max_length=50)
    schedule = models.CharField(max_length=50)
    days = ArrayField(models.CharField(max_length=50))
    _class = models.IntegerField()
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, related_name='classes')

    def __str__(self):
        return self._class
