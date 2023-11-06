from typing import Any
from django.core.management.base import BaseCommand
from api.utils import sessions, web_scraping, db_handler
from time import time

class Command(BaseCommand):
    """Comando para atualizar o banco de dados."""

    help = "Atualiza o banco de dados com as disciplinas do SIGAA e suas respectivas turmas."

    def handle(self, *args: Any, **options: Any):
        departments_ids = web_scraping.get_list_of_departments()

        if departments_ids is None:
            self.display_error_message("department_ids")
            return

        print("Atualizando o banco de dados...")

        # Obtem o ano e o período atual e o ano e o período seguinte
        previous_period_year, previous_period = sessions.get_previous_period()
        current_year, current_period = sessions.get_current_year_and_period()
        next_period_year, next_period = sessions.get_next_period()

        # Apaga as disciplinas do período interior
        db_handler.delete_all_departments_using_year_and_period(previous_period_year, previous_period)

        # Atualiza as disciplinas do período atual
        start_time = time()
        self.update_departments(departments_ids=departments_ids, year=current_year, period=current_period)
        self.display_success_message(operation=f"{current_year}/{current_period}", start_time=start_time)

        # Atualiza as disciplinas do período seguinte
        start_time = time()
        self.update_departments(departments_ids=departments_ids, year=next_period_year, period=next_period)
        self.display_success_message(operation=f"{next_period_year}/{next_period}", start_time=start_time)

    def update_departments(self, departments_ids: list, year: str, period: str) -> None:
        for department_id in departments_ids:
            disciplines_list = web_scraping.get_department_disciplines(department_id=department_id, current_year=year, current_period=period)
            department = db_handler.create_department(code=department_id, year=year, period=period)

            # Para cada disciplina do período atual, deleta as turmas previamente cadastradas e cadastra novas turmas no banco de dados
            for discipline_code in disciplines_list:
                classes_info = disciplines_list[discipline_code]

                # Cria ou pega a disciplina
                discipline = db_handler.create_discipline(name=classes_info[0]["name"], code=discipline_code, department=department)
                # Deleta as turmas previamente cadastradas
                db_handler.delete_classes_from_discipline(discipline=discipline)

                # Cadastra as novas turmas
                for class_info in classes_info:
                    db_handler.create_class(workload=class_info["workload"], teachers=class_info["teachers"],
                                            classroom=class_info["classroom"], schedule=class_info["schedule"],
                                            days=class_info["days"], _class=class_info["class_code"], discipline=discipline)

    def display_error_message(self, operation: str) -> None:
        print("Não foi possível realizar a operação de atualização do banco de dados.")
        print("Verifique se o SIGAA está funcionando corretamente.")
        print(f"Falha em {operation}", end="\n\n")

    def display_success_message(self, operation: str, start_time: float) -> None:
        print("Operação de atualização do banco de dados realizada com sucesso.")
        print(f"Sucesso em {operation}")
        print(f"Tempo de execução: {(time() - start_time):.1f}s", end="\n\n")
