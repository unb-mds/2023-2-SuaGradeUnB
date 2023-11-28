from utils import db_handler as dbh
from rest_framework.decorators import APIView
from utils.sessions import get_current_year_and_period, get_next_period
from rest_framework import status, request, response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api import serializers

MAXIMUM_RETURNED_DISCIPLINES = 5
ERROR_MESSAGE = "no valid argument found for 'search', 'year' or 'period'"


class Search(APIView):

    def treat_string(self, string: str | None) -> str | None:
        if string is not None:
            string = string.strip()

        return string

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
            400: openapi.Response('BAD_REQUEST', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'errors': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Mensagem de erro'
                    ),
                }
            )),
        }
    )
    def get(self, request: request.Request, *args, **kwargs) -> response.Response:
        name = self.treat_string(request.GET.get('search', None))
        year = self.treat_string(request.GET.get('year', None))
        period = self.treat_string(request.GET.get('period', None))

        if name is None or len(name) == 0 or year is None or len(year) == 0 or period is None or len(period) == 0:
            return response.Response(
                {
                    "errors": ERROR_MESSAGE
                }, status.HTTP_400_BAD_REQUEST)

        name = name.split()
        disciplines = dbh.filter_disciplines_by_name(name=name[0])

        for term in name[1:]:
            disciplines &= dbh.filter_disciplines_by_name(name=term)

        if not disciplines.count():
            disciplines = dbh.filter_disciplines_by_code(code=name[0])

            for term in name[1:]:
                disciplines &= dbh.filter_disciplines_by_code(code=term)

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
