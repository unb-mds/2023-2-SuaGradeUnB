from rest_framework.serializers import ModelSerializer
from api.models import Department, Discipline, Class

class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = Department
        fields = ('code', 'year', 'period')

class ClassSerializer(ModelSerializer):
    class Meta:
        model = Class
        fields = ('workload', 'teachers', 'classroom', 'schedule', 'days', '_class')

class DisciplineSerializer(ModelSerializer):
    department = DepartmentSerializer()
    classes = ClassSerializer(many=True)
    
    class Meta:
        model = Discipline
        fields = ('name', 'code', 'department', 'classes')