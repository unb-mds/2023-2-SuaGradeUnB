from django.contrib import admin
from .models import Department, Discipline, Class, Schedule

from utils.json_pretty import json_prettify


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'year', 'period']
    search_fields = ['code', 'name']
    ordering = ['year', 'period', 'name']


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


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']
    exclude = ('classes', )
    readonly_fields = ('classes_pretty', )
    ordering = ['id']

    def classes_pretty(self, obj):
        return json_prettify(obj.classes)

    classes_pretty.short_description = 'Classes'
