from rest_framework.serializers import ModelSerializer
from api.models import Department, Discipline, Class

class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
class ClassSerializer(ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'

class DisciplineSerializer(ModelSerializer):
    department = DepartmentSerializer()
    classes = ClassSerializer(many=True)
    
    class Meta:
        model = Discipline
        fields = '__all__'