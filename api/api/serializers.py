from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from api.models import Department, Discipline, Class, Schedule
import utils.db_handler as dbh


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

    def get_classes(self, discipline: Discipline):
        teacher_name = self.context.get('teacher_name')
        schedule = self.context.get('schedule')
        classes = discipline.classes.all() if hasattr(
            discipline, 'classes') else Class.objects.none()
        if teacher_name:
            classes = dbh.filter_classes_by_teacher(
                name=teacher_name, classes=classes)
        if schedule:
            classes = dbh.filter_classes_by_schedule(
                schedule=schedule, classes=classes)
        return ClassSerializer(classes, many=True).data


class ClassSerializerSchedule(ClassSerializer):
    discipline = DisciplineSerializerSchedule()


class ScheduleSerializer(ModelSerializer):
    class Meta:
        model = Schedule
        exclude = ['user']


class GenerateSchedulesSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=200)
    schedules = ClassSerializerSchedule(many=True)
