from utils.db_handler import filter_disciplines_by_name, filter_disciplines_by_code, filter_disciplines_by_year_and_period
from rest_framework.decorators import APIView
from .serializers import DisciplineSerializer
from utils.sessions import get_current_year_and_period, get_next_period
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

MAXIMUM_RETURNED_DISCIPLINES = 5
ERROR_MESSAGE = "no valid argument found for 'search', 'year' or 'period'"


class Search(APIView):
    def treat_string(self, string: str | None) -> str | None:
        if string is not None:
            string = string.strip()

        return string

    def get(self, request: Request, *args, **kwargs) -> Response:
        name = self.treat_string(request.GET.get('search', None))
        year = self.treat_string(request.GET.get('year', None))
        period = self.treat_string(request.GET.get('period', None))

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


class YearPeriod(APIView):
    def get(self, request: Request, *args, **kwargs) -> Response:
        year, period = get_current_year_and_period()
        next_year, next_period = get_next_period()

        data = {
            'year/period': [f'{year}/{period}', f'{next_year}/{next_period}'],
        }

        return Response(data, status.HTTP_200_OK)
