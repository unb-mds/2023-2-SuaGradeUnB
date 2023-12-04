from utils import db_handler as dbh
from .models import Discipline
from unidecode import unidecode
from django.contrib import admin
from django.db.models.query import QuerySet
from rest_framework.decorators import APIView
from utils.sessions import get_current_year_and_period, get_next_period
from rest_framework import status, request, response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .swagger import Errors
from api import serializers
from utils.schedule_generator import ScheduleGenerator

MAXIMUM_RETURNED_DISCIPLINES = 8
ERROR_MESSAGE = "no valid argument found for 'search', 'year' or 'period'"
MINIMUM_SEARCH_LENGTH = 4
ERROR_MESSAGE_SEARCH_LENGTH = f"search must have at least {MINIMUM_SEARCH_LENGTH} characters"


class Search(APIView):

    def treat_string(self, string: str | None) -> str | None:
        if string is not None:
            string = string.strip()

        return string

    def filter_disciplines(self, request: request.Request, name: str) -> QuerySet[Discipline]:
        unicode_name = unidecode(name).casefold()

        model_handler = admin.ModelAdmin(Discipline, admin.site)
        model_handler.search_fields = ['unicode_name', 'code']

        disciplines = Discipline.objects.all()
        disciplines, _ = model_handler.get_search_results(
            request, disciplines, unicode_name)

        return disciplines

    @swagger_auto_schema(
        operation_description="Busca disciplinas por nome ou código. O ano e período são obrigatórios.",
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY,
                              description="Termo de pesquisa (Nome/Código)", type=openapi.TYPE_STRING),
            openapi.Parameter('year', openapi.IN_QUERY,
                              description="Ano", type=openapi.TYPE_INTEGER),
            openapi.Parameter('period', openapi.IN_QUERY,
                              description="Período  ", type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: openapi.Response('OK', serializers.DisciplineSerializer),
            **Errors([400]).retrieve_erros()
        }
    )
    def get(self, request: request.Request, *args, **kwargs) -> response.Response:
        name = self.treat_string(request.GET.get('search', None))
        year = self.treat_string(request.GET.get('year', None))
        period = self.treat_string(request.GET.get('period', None))

        name_verified = name is not None and len(name) > 0
        year_verified = year is not None and len(year) > 0
        period_verified = period is not None and len(period) > 0

        if not name_verified or not year_verified or not period_verified:
            return response.Response(
                {
                    "errors": ERROR_MESSAGE
                }, status.HTTP_400_BAD_REQUEST)

        if len(name) < MINIMUM_SEARCH_LENGTH:
            return response.Response(
                {
                    "errors": ERROR_MESSAGE_SEARCH_LENGTH
                }, status.HTTP_400_BAD_REQUEST)

        disciplines = self.filter_disciplines(request, name)
        disciplines = dbh.get_best_similarities_by_name(name, disciplines)

        if not disciplines.count():
            disciplines = dbh.filter_disciplines_by_code(code=name[0])

            for term in name[1:]:
                disciplines &= dbh.filter_disciplines_by_code(code=term)

            disciplines = dbh.filter_disciplines_by_code(name)

        filtered_disciplines = dbh.filter_disciplines_by_year_and_period(
            year=year, period=period, disciplines=disciplines)
        data = serializers.DisciplineSerializer(
            filtered_disciplines, many=True).data

        return response.Response(data[:MAXIMUM_RETURNED_DISCIPLINES], status.HTTP_200_OK)


class YearPeriod(APIView):

    @swagger_auto_schema(
        operation_description="Retorna o ano e período atual, e o próximo ano e período letivos válidos para pesquisa.",
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

class Schedule(APIView):
    def post(self, request: request.Request, *args, **kwargs) -> response.Response:
        classes_id = request.data.get('classes', None)
        preference = request.data.get('preference', None)
        preference_valid = preference is not None and isinstance(preference, list) and all(isinstance(x, int) for x in preference) and len(preference) == 3
        
        if preference is not None and not preference_valid:
            return response.Response(
                {
                    "errors": "preference must be a list of 3 integers"
                }, status.HTTP_400_BAD_REQUEST)

        if classes_id is None:
            return response.Response(
                {
                    "errors": "classes is required"
                }, status.HTTP_400_BAD_REQUEST)

        schedule_generator = ScheduleGenerator(classes_id, preference)
        schedules = schedule_generator.generate()

        if schedules is None:
            return response.Response(
                {
                    "errors": "classes must be a list of valid classes id."
                }, status.HTTP_400_BAD_REQUEST)
        
        data = []
        
        for schedule in schedules:
            data.append(list(map(lambda x: serializers.ClassSerializerSchedule(x).data, schedule)))

        return response.Response(data, status.HTTP_200_OK)