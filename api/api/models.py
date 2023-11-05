from django.db import models
from django.contrib.postgres.fields import ArrayField

class Department(models.Model):
    # Classe que representa um departamento
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

class Discipline(models.Model):
    # Classe que representa uma disciplina
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10, unique=True)
    workload = models.IntegerField()
    teachers = ArrayField(models.CharField(max_length=50))
    classroom = models.CharField(max_length=50)
    schedule = models.CharField(max_length=50)
    days = ArrayField(models.CharField(max_length=50))
    _class = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='disciplines')

    def __str__(self):
        return self.name