from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, request, response

from api.swagger import Errors
from api.serializers import ScheduleSerializer

from utils.db_handler import get_schedules

class GetSchedules(APIView):
    
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Retorna as grades horárias do usuário logado.",
        security=[{'Bearer': []}],
        responses={
            200: openapi.Response('OK', ScheduleSerializer(many=True)),
            **Errors([401, 403]).retrieve_erros()
        }
    )
    def get(self, request: request.Request) -> response.Response:
        """Retorna as grades horárias do usuário logado."""
        
        user = request.user
        schedules = get_schedules(user)
        data = ScheduleSerializer(schedules, many=True).data
        
        return response.Response(status=status.HTTP_200_OK, data=data)