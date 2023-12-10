from utils import db_handler as dbh

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status, request, response

from api.swagger import Errors


class DeleteSchedule(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Deleta a grade horária do usuário logado.",
        security=[{'Bearer': []}],
        responses={
            204: openapi.Response('NO CONTENT'),
            **Errors([400, 401, 403]).retrieve_erros()
        }
    )
    def delete(self, request: request.Request, id: int) -> response.Response:
        """Delete a grade horária do usuário logado."""
        user = request.user

        return response.Response(status=status.HTTP_204_NO_CONTENT) if dbh.delete_schedule(user, id) else response.Response(status=status.HTTP_400_BAD_REQUEST)
