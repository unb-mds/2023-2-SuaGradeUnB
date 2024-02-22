from django.db import models
from unidecode import unidecode
from django.contrib.postgres.fields import ArrayField
from users.models import User
from django.utils import timezone
from django.core.cache import cache

cache_error_msg = "Cache isn't working properly, so database isn't allowed to be modified!"


class CustomModel(models.Model):
    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        try:
            cache.delete(kwargs['cache_key'])
            kwargs.pop('cache_key')
        except:  # pragma: no cover
            raise ValueError(cache_error_msg)
        else:
            super(CustomModel, self).delete()
            pass


class Department(CustomModel):
    """Classe que representa um departamento.
    code:str -> Código do departamento
    year:str -> Ano do departamento
    period:str -> Período do departamento
    """
    name = models.CharField(max_length=128, default='')
    code = models.CharField(max_length=10)
    year = models.CharField(max_length=4, default='0000')
    period = models.CharField(max_length=1, default='1')

    def __str__(self):
        return self.code

    def get_cache_key(self):
        code = self.code
        year = self.year
        period = self.period

        return f"{code}/{year}.{period}"

    def delete(self, *args, **kwargs):
        kwargs['cache_key'] = self.get_cache_key()
        super(Department, self).delete(*args, **kwargs)


class Discipline(CustomModel):
    """Classe que representa uma disciplina.
    name:str -> Nome da disciplina
    unicode_name:str -> Nome da disciplina normalizado
    code:str -> Código da disciplina
    department:Department -> Departamento da disciplina
    """
    name = models.CharField(max_length=128)
    unicode_name = models.CharField(max_length=128, default='')
    code = models.CharField(max_length=64)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name='disciplines')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.unicode_name = unidecode(self.name).casefold()
        super(Discipline, self).save(*args, **kwargs)

    def get_cache_key(self):
        code = self.department.code
        year = self.department.year
        period = self.department.period

        return f"{code}/{year}.{period}"

    def delete(self, *args, **kwargs):
        kwargs['cache_key'] = self.get_cache_key()
        super(Discipline, self).delete(*args, **kwargs)


class Class(CustomModel):
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
    discipline = models.ForeignKey(
        Discipline, on_delete=models.CASCADE, related_name='classes')

    special_dates = ArrayField(
        ArrayField(
            models.CharField(max_length=256),
            size=3,
        ),
        default=list
    )

    def __str__(self):
        return self._class

    def get_cache_key(self):
        code = self.discipline.department.code
        year = self.discipline.department.year
        period = self.discipline.department.period

        return f"{code}/{year}.{period}"

    def delete(self, *args, **kwargs):
        kwargs['cache_key'] = self.get_cache_key()
        super(Class, self).delete(*args, **kwargs)


class Schedule(models.Model):
    """Classe que representa um horário.
    user:User -> Usuário do horário
    classes:list -> Lista de turmas do horário
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='schedules')
    classes = models.JSONField(default=list)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Class: {self.id} - User: {self.user.email}'
