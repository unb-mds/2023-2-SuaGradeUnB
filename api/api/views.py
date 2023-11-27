from utils.db_handler import filter_disciplines_by_year_and_period
from .models import Discipline
from unidecode import unidecode
from django.contrib import admin
from django.db.models.query import QuerySet
from rest_framework.decorators import APIView
from .serializers import DisciplineSerializer
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

MAXIMUM_RETURNED_DISCIPLINES = 8
ERROR_MESSAGE = "no valid argument found for 'search', 'year' or 'period'"
MINIMUM_SEARCH_LENGTH = 4
ERROR_MESSAGE_SEARCH_LENGTH = f"search must have at least {MINIMUM_SEARCH_LENGTH} characters"


class Search(APIView):
    def treat_string(self, string: str | None) -> str | None:
        if string is not None:
            string = string.strip()

        return string
    
    def filter_disciplines(self, request: Request, name: str) -> QuerySet[Discipline]:
        model_handler = admin.ModelAdmin(Discipline, admin.site)
        model_handler.search_fields = ['unicode_name', 'code']

        disciplines = Discipline.objects.all()
        disciplines, _ = model_handler.get_search_results(request, disciplines, name)

        return disciplines


    def get(self, request: Request, *args, **kwargs) -> Response:
        name = self.treat_string(request.GET.get('search', None))
        year = self.treat_string(request.GET.get('year', None))
        period = self.treat_string(request.GET.get('period', None))

        name_verified = name is not None and len(name) > 0
        year_verified = year is not None and len(year) > 0
        period_verified = period is not None and len(period) > 0

        if not name_verified or not year_verified or not period_verified:
            return Response(
                {
                    "errors": ERROR_MESSAGE
                }, status.HTTP_400_BAD_REQUEST)

        if len(name) < MINIMUM_SEARCH_LENGTH:
            return Response(
                {
                    "errors": ERROR_MESSAGE_SEARCH_LENGTH
                }, status.HTTP_400_BAD_REQUEST)

        disciplines = self.filter_disciplines(request, unidecode(name).casefold())

        filtered_disciplines = filter_disciplines_by_year_and_period(
            year=year, period=period, disciplines=disciplines)
        data = DisciplineSerializer(filtered_disciplines, many=True).data

        return Response(data[:MAXIMUM_RETURNED_DISCIPLINES], status.HTTP_200_OK)
