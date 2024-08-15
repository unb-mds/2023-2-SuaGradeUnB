from ..models import Discipline, Class

from django.db.models.query import QuerySet

from rest_framework.decorators import APIView
from rest_framework import status, request, response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from utils.sessions import get_current_year_and_period, get_next_period
from utils.schedule_generator import ScheduleGenerator
from utils.db_handler import get_best_similarities_by_name, filter_disciplines_by_teacher, filter_disciplines_by_year_and_period, filter_disciplines_by_code, filter_disciplines_by_schedule_and_department_code
from utils.search import SearchTool

from .. import serializers
from api.swagger import Errors
from api.models import Discipline
from api.views.utils import handle_400_error

from traceback import print_exception

MAXIMUM_RETURNED_DISCIPLINES = 15
ERROR_MESSAGE = "Bad search parameters or missing parameters"
MINIMUM_SEARCH_LENGTH = 4
ERROR_MESSAGE_SEARCH_LENGTH = f"search must have at least {MINIMUM_SEARCH_LENGTH} characters"
MAXIMUM_RETURNED_SCHEDULES = 5


class Search(APIView):

    def treat_string(self, string: str | None) -> str | None:
        if string is not None:
            string = string.strip()

        return string

    def filter_disciplines(self, request: request.Request, name: str) -> QuerySet[Discipline]:
        search_handler = SearchTool(Discipline)
        search_fields = ['unicode_name', 'code']

        result = search_handler.filter_by_search_result(
            request=request,
            search_str=name,
            search_fields=search_fields
        )

        return result

    def retrieve_disciplines_by_similarity(self, request: request.Request, name: str) -> QuerySet[Discipline]:
        disciplines = self.filter_disciplines(request, name)

        disciplines = get_best_similarities_by_name(name, disciplines)
        if not disciplines.count():
            disciplines = filter_disciplines_by_code(code=name[0])
            for term in name[1:]:
                disciplines &= filter_disciplines_by_code(code=term)

            disciplines = filter_disciplines_by_code(name)

        return disciplines

    def get_disciplines_and_search_flag(self, request, name):
        disciplines = self.retrieve_disciplines_by_similarity(request, name)
        search_by_teacher = False
        if not disciplines.count():
            disciplines = filter_disciplines_by_teacher(name)
            search_by_teacher = True
        return disciplines, search_by_teacher

    def get_serialized_data(self, filter_params: dict, search_by_teacher: bool, name: str, schedule=None, search_by_schedule=False) -> list:
        filtered_disciplines = filter_disciplines_by_year_and_period(
            **filter_params)
        if search_by_teacher:
            data = serializers.DisciplineSerializer(
                filtered_disciplines, many=True, context={'teacher_name': name}).data
        elif search_by_schedule:
            data = serializers.DisciplineSerializer(
                filtered_disciplines, many=True, context={'schedule': schedule}).data
        else:
            data = serializers.DisciplineSerializer(
                filtered_disciplines, many=True).data
        return data

    def get_request_parameters(self, request):
        name = self.treat_string(request.GET.get('search', None))
        year = self.treat_string(request.GET.get('year', None))
        period = self.treat_string(request.GET.get('period', None))
        department_code = self.treat_string(
            request.GET.get('department_code', None))
        schedule = self.treat_string(request.GET.get('schedule', None))
        return name, year, period, schedule, department_code

    @ swagger_auto_schema(
        operation_description="Busca disciplinas por nome ou código. O ano e período são obrigatórios.",
        security=[],
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY,
                              description="Termo de pesquisa (Nome/Código/Professor)", type=openapi.TYPE_STRING),
            openapi.Parameter('year', openapi.IN_QUERY,
                              description="Ano", type=openapi.TYPE_INTEGER),
            openapi.Parameter('period', openapi.IN_QUERY,
                              description="Período  ", type=openapi.TYPE_INTEGER),
            openapi.Parameter('department_code', openapi.IN_QUERY,
                              description="Código do departamento", type=openapi.TYPE_STRING),
            openapi.Parameter('schedule', openapi.IN_QUERY,
                              description="Horário no formato 46M34", type=openapi.TYPE_STRING)
        ],
        responses={
            200: openapi.Response('OK', serializers.DisciplineSerializer),
            **Errors([400]).retrieve_erros()
        }
    )
    def get(self, request: request.Request, *args, **kwargs) -> response.Response:
        name, year, period, schedule, department_code = self.get_request_parameters(
            request)
        if not all((year, period)):
            return handle_400_error(ERROR_MESSAGE)
        disciplines, search_by_teacher, search_by_schedule = None, False, False
        if name:
            if len(name) < MINIMUM_SEARCH_LENGTH:
                return handle_400_error(ERROR_MESSAGE_SEARCH_LENGTH)
            disciplines, search_by_teacher = self.get_disciplines_and_search_flag(
                request, name)
            if schedule:
                search_by_schedule = True
        elif schedule and department_code:
            disciplines = filter_disciplines_by_schedule_and_department_code(
                schedule=schedule, department_code=department_code)
            search_by_schedule = True
        else:
            return handle_400_error(ERROR_MESSAGE)

        data = self.get_serialized_data(
            filter_params={'year': year, 'period': period,
                           'disciplines': disciplines},
            search_by_teacher=search_by_teacher,
            search_by_schedule=search_by_schedule,
            name=name,
            schedule=schedule
        )

        data_aux = []
        for i in range(len(data)):
            if data[i]['classes'] == []:
                data_aux.append(data[i])
        for i in data_aux:
            data.remove(i)
        return response.Response(data[:MAXIMUM_RETURNED_DISCIPLINES], status.HTTP_200_OK)


class YearPeriod(APIView):

    @ swagger_auto_schema(
        operation_description="Retorna o ano e período atual, e o próximo ano e período letivos válidos para pesquisa.",
        security=[],
        responses={
            200: openapi.Response('OK', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'year/period': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_STRING
                        )
                    )
                }
            ), examples={
                'application/json': {
                    'year/period': ['2020/1', '2020/2']
                }
            })
        }
    )
    def get(self, request: request.Request, *args, **kwargs) -> response.Response:
        year, period = get_current_year_and_period()
        next_year, next_period = get_next_period()

        data = {
            'year/period': [f'{year}/{period}', f'{next_year}/{next_period}'],
        }

        return response.Response(data, status.HTTP_200_OK)


class GenerateSchedule(APIView):
    @ swagger_auto_schema(
        operation_description="Gera possíveis horários de acordo com as aulas escolhidas com preferência de turno",
        security=[],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            title="body",
            required=['classes'],
            properties={
                'classes': openapi.Schema(
                    description="Lista de ids de aulas escolhidas",
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        description="Id da aula",
                        type=openapi.TYPE_INTEGER
                    )
                ),
                'preference': openapi.Schema(
                    description="Lista de preferências (manhã, tarde, noite)",
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        description="Define o peso de cada turno",
                        type=openapi.TYPE_INTEGER,
                        enum=[1, 2, 3]
                    )
                )
            }
        ),
        responses={
            200: serializers.GenerateSchedulesSerializer(many=True),
            **Errors([400]).retrieve_erros()
        }
    )
    def post(self, request: request.Request, *args, **kwargs) -> response.Response:
        """
        View para gerar horários.
        Funcionamento: Recebe uma lista de ids de classes e uma lista de preferências
        e verifica se as classes e preferências são válidas.
        Caso sejam válidas, gera os horários e retorna uma lista de horários.
        """

        classes_id = request.data.get('classes', None)
        preference = request.data.get('preference', None)
        preference_valid = preference is not None and isinstance(preference, list) and all(
            isinstance(x, int) for x in preference) and len(preference) == 3
        classes_valid = classes_id is not None and isinstance(
            classes_id, list) and all(isinstance(x, int) for x in classes_id) and len(classes_id) > 0

        if preference is not None and not preference_valid:
            """Retorna um erro caso a preferência não seja uma lista de 3 inteiros"""
            return response.Response(
                {
                    "errors": "preference must be a list of 3 integers"
                }, status.HTTP_400_BAD_REQUEST)

        if not classes_valid:
            """Retorna um erro caso a lista de ids de classes não seja enviada"""
            return response.Response(
                {
                    "errors": "classes is required and must be a list of integers with at least one element"
                }, status.HTTP_400_BAD_REQUEST)

        try:
            schedule_generator = ScheduleGenerator(classes_id, preference)
            generated_data = schedule_generator.generate()
        except Exception as error:
            """Retorna um erro caso ocorra algum erro ao criar o gerador de horários"""

            message_error = "An internal error has occurred."

            if type(error) is ValueError:
                message_error = str(error)
            else:  # pragma: no cover
                print_exception(error)

            return response.Response(
                {
                    "errors": message_error
                }, status.HTTP_400_BAD_REQUEST)

        schedules = generated_data.get("schedules", [])
        message = generated_data.get("message", "")
        data = []

        for schedule in schedules[:MAXIMUM_RETURNED_SCHEDULES]:
            data.append(
                list(map(lambda x: serializers.ClassSerializerSchedule(x).data, schedule)))

        return response.Response({
            'message': message,
            'schedules': data
        }, status.HTTP_200_OK)
