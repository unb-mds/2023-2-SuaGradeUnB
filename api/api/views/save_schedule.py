from utils.schedule_generator import ScheduleGenerator
from utils import db_handler as dbh

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status, request, response

from api.models import Class
from api.swagger import Errors
from api import serializers


class SaveSchedule(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Salva uma grade horária para o usuário logado.",
        request_body=serializers.ClassSerializerSchedule(many=True),
        security=[{'Bearer': []}],
        responses={
            201: openapi.Response('CREATED'),
            **Errors([400, 401, 403]).retrieve_erros()
        }
    )
    def post(self, request: request.Request, *args, **kwargs) -> response.Response:
        classes = request.data

        unique_year_period = set()
        current_db_classes_ids = []

        classes_viability = check_classes_viability(
            classes,
            unique_year_period,
            current_db_classes_ids
        )
        if classes_viability:
            return classes_viability

        if len(unique_year_period) > 1:
            return handle_400_error("all classes must have the same year and period")

        try:
            valid_schedule = validate_received_schedule(current_db_classes_ids)
        except:
            error_msg = "error while saving schedule, you may have chosen classes that are not compatible"
            return handle_400_error(error_msg)

        user = request.user
        answer = dbh.save_schedule(user, valid_schedule)

        return response.Response(status=status.HTTP_201_CREATED) if answer else handle_400_error("error while saving schedule")


def check_classes_viability(classes: list[dict], unique_year_period: set, current_db_classes_ids: list[int]):
    for _class in classes:
        key_args = retrieve_important_params_from_class(_class)

        year_period = retrieve_year_period_from_class(_class)
        unique_year_period.add(year_period)

        db_class = dbh.get_class_by_params(**key_args)
        if not db_class:
            code = retrieve_discipline_code_from_class(_class)
            error_msg = f"the class {code} does not exists with this params"
            return handle_400_error(error_msg)

        current_db_classes_ids.append(db_class.id)


def retrieve_year_period_from_class(_class: dict) -> tuple:
    department = _class.get('discipline').get('department')
    year, period = department.get('year'), department.get('period')

    return year, period


def retrieve_discipline_code_from_class(_class: dict) -> str:
    discipline = _class.get('discipline')
    code = discipline.get('code')

    return code


def retrieve_important_params_from_class(_class: dict) -> dict:
    discipline = _class.get('discipline')
    name = discipline.get('name')
    code = retrieve_discipline_code_from_class(_class)

    year, period = retrieve_year_period_from_class(_class)

    schedule, days = _class.get('schedule'), _class.get('days')
    special_dates = _class.get('special_dates')

    classroom = _class.get('classroom')
    teachers = _class.get('teachers')

    key_args = {
        'discipline__name': name, 'discipline__code': code,
        'discipline__department__year': year,
        'discipline__department__period': period,
        'schedule': schedule, 'days': days,
        'special_dates': special_dates,
        'classroom': classroom,
        'teachers': teachers
    }

    return key_args


def handle_400_error(error_msg: str) -> response.Response:
    return response.Response(
        {
            "errors": error_msg
        }, status.HTTP_400_BAD_REQUEST)


def validate_received_schedule(classes_id: list[int]) -> list[Class]:
    schedule_generator = ScheduleGenerator(classes_id)
    schedules = schedule_generator.generate()

    if len(schedules) != 1:
        raise ValueError("the classes are not compatible")

    return schedules[0]
