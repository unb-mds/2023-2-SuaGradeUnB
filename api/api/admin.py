from django.contrib import admin
from .models import Department, Discipline, Class


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['code', 'year', 'period']
    search_fields = ['code']
    ordering = ['year', 'period']


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']
    ordering = ['name']


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['discipline', 'classroom', 'schedule']
    search_fields = ['discipline__name']
    ordering = ['discipline__name']
