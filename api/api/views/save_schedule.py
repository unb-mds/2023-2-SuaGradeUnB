from utils.schedule_generator import ScheduleGenerator
from utils import db_handler as dbh

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status, request, response

from api.models import Class
from api.swagger import Errors
from api.views.utils import handle_400_error
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

        try:
            validate_request_body_structure(classes)
        except ValueError as e:
            return handle_400_error(e.args[0])

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


def check_discipline_key_existence(key: str, discipline_key: str, **kwargs):
    _class = kwargs.get('_class')

    if discipline_key not in _class[key].keys():
        raise ValueError(f"the discipline must have the {discipline_key} key")


def check_department_key_existence(department_keys: list[str], **kwargs):
    _class = kwargs.get('_class')

    for department_key in department_keys:
        if department_key not in _class['discipline']['department'].keys():
            raise ValueError(
                f"the department must have the {department_key} key")


def check_disciplines(key, **kwargs):
    _class = kwargs.get('_class')
    discipline_keys = kwargs.get('expected_discipline_keys')
    department_keys = kwargs.get('expected_department_keys')

    for discipline_key in discipline_keys:
        check_discipline_key_existence(key, discipline_key, **kwargs)

        if discipline_key == 'department':
            if not isinstance(_class['discipline']['department'], dict):
                raise ValueError(
                    "the department must be a object structure")

            check_department_key_existence(department_keys, **kwargs)


def validate_class(**kwargs) -> response.Response | None:
    _class = kwargs.get('_class')
    expected_keys = kwargs.get('expected_keys')

    for key in expected_keys:
        if key not in _class.keys():
            raise ValueError(f"the class must have the {key} key")

        if key == 'discipline':
            if not isinstance(_class[key], dict):
                raise ValueError("the discipline must be a object structure")

            check_disciplines(key, **kwargs)


def validate_request_body_structure(body: list[dict] | None) -> bool:
    if not body:
        raise ValueError("the request body must not be empty")

    if not isinstance(body, list):
        raise ValueError("the request body must be a list of classes")

    for _class in body:
        if not isinstance(_class, dict):
            raise ValueError("each class must be a object structure")

        expected_keys = ['discipline', 'schedule', 'days',
                         'special_dates', 'classroom', 'teachers']
        expected_discipline_keys = ['name', 'code', 'department']
        expected_department_keys = ['year', 'period']
        args = {
            '_class': _class,
            'expected_keys': expected_keys,
            'expected_discipline_keys': expected_discipline_keys,
            'expected_department_keys': expected_department_keys
        }
        validate_class(**args)


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


def validate_received_schedule(classes_id: list[int]) -> list[Class]:
    schedule_generator = ScheduleGenerator(classes_id)
    schedules = schedule_generator.generate()

    if len(schedules) != 1:
        raise ValueError("the classes are not compatible")

    return schedules[0]
