from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from api.models import Department, Discipline, Class, Schedule


class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class ClassSerializer(ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'


class DisciplineSerializerSchedule(ModelSerializer):
    department = DepartmentSerializer()

    class Meta:
        model = Discipline
        fields = '__all__'


class DisciplineSerializer(DisciplineSerializerSchedule):
    classes = serializers.SerializerMethodField()

    def get_classes(self, obj):
        teacher_name = self.context.get('teacher_name')
        classes = obj.classes.all() if hasattr(
            obj, 'classes') else Class.objects.none()
        if teacher_name:
            classes = classes.filter(teachers__icontains=teacher_name)

        return ClassSerializer(classes, many=True).data


class ClassSerializerSchedule(ClassSerializer):
    discipline = DisciplineSerializerSchedule()


class ScheduleSerializer(ModelSerializer):
    class Meta:
        model = Schedule
        exclude = ['user']
