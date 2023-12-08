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

from .save_schedule import SaveSchedule

class Schedules(APIView, SaveSchedule):
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        """
        Instancia e retorna a lista de permissões que serão usadas por esta view.
        """
        if self.request.method in ['GET', 'POST']:
            return [permission() for permission in self.permission_classes]
        else: # pragma: no cover
            return []
        
    @swagger_auto_schema(
        operation_description="Retorna as grades horárias do usuário logado.",
        security=[{'Bearer': []}],
        responses={
            200: openapi.Response('OK', serializers.ScheduleSerializer(many=True)),
            **Errors([401, 403]).retrieve_erros()
        }
    )
    def get(self, request: request.Request, **kwargs) -> response.Response:
        """Retorna as grades horárias do usuário logado."""
        
        user = request.user
        schedules = dbh.get_schedules(user)
        data = serializers.ScheduleSerializer(schedules, many=True).data
        
        return response.Response(status=status.HTTP_200_OK, data=data)