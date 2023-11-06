from typing import Any
from django.core.management.base import BaseCommand
from api.utils import sessions, web_scraping
from api.models import Discipline, Department
from decouple import config

"""Comando para atualizar o banco de dados."""
class Command(BaseCommand):
    help = "Atualiza o banco de dados com as disciplinas do SIGAA e suas respectivas turmas."

    def handle(self, *args: Any, **options: Any):
        departments_ids = web_scraping.get_list_of_departments() #Obtem os códigos dos departamentos

        if departments_ids is None:
            self.display_error_message("department_ids") #Exibe uma mensagem de erro caso não seja possível obter os códigos dos departamentos
            return

        # Obtem o ano e o período atual e o ano e o período seguinte
        current_year, current_period = sessions.get_current_year_and_period()
        next_period_year, next_period = sessions.get_next_period()


    def display_error_message(self, operation: str) -> None:
        print("Não foi possível realizar a operação de atualização do banco de dados.")
        print("Verifique se o SIGAA está funcionando corretamente.")
        print(f"Falha em {operation}")
