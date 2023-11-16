from utils.db_handler import filter_disciplines_by_name, filter_disciplines_by_code, filter_disciplines_by_year_and_period
from rest_framework.decorators import APIView
from .serializers import DisciplineSerializer
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.db.models import QuerySet

MAXIMUM_RETURNED_DISCIPLINES = 5
ERROR_MESSAGE = "no valid argument found for 'search', 'year' or 'period'"


class Search(APIView):
    def get(self, request: Request, *args, **kwargs) -> Response:
        name = request.GET.get('search', None)
        year = request.GET.get('year', None)
        period = request.GET.get('period', None)

        if name is None or len(name) == 0 or year is None or len(year) == 0 or period is None or len(period) == 0:
            return Response(
                {
                    "errors": ERROR_MESSAGE
                }, status.HTTP_400_BAD_REQUEST)

        name = name.split()
        disciplines = filter_disciplines_by_name(name=name[0])

        for term in name[1:]:
            disciplines &= filter_disciplines_by_name(name=term)

        if not disciplines.count():
            disciplines = filter_disciplines_by_code(code=name[0])

            for term in name[1:]:
                disciplines &= filter_disciplines_by_code(code=term)
            
        filtered_disciplines = filter_disciplines_by_year_and_period(
            year=year, period=period, disciplines=disciplines)
        data = DisciplineSerializer(filtered_disciplines, many=True).data

        return Response(data[:MAXIMUM_RETURNED_DISCIPLINES], status.HTTP_200_OK)
